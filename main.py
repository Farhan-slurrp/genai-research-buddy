from collections import deque
import json
import ollama
import src.formatter as formatter
import src.filereader as filereader
import src.websearch as websearch
import src.webscrapper as webscrapper

llm = "qwen2.5"
list_tools = [filereader.tool_read_file, websearch.tool_search_web, webscrapper.tool_scrape_webpage]


prompt = '''
You are a research assistant that will help researcher(s) with their research.

You MUST follow these guidelines in answering and helping the researcher:
1. You have access to tools and use multiple tools in answering the researcher input, you must decide when to use tools to answer the researcher's message.
2. You can give details, try to help the researcher understand the whole concepts that you are saying.
3. DON'T HALLUCINATE! and answer in researcher's language.

That's it for now. Be the best scholar to make researcher happy.
''' 
messages = [{"role":"system", "content":prompt}]

while True:
    try:
        q = input('😃 > ')
    except EOFError:
        break
    if q == "quit":
        break
    if q.strip() == "":
        continue
    messages.append( {"role":"user", "content":q} )
   
    agent_res = ollama.chat(
        model=llm,
        tools=list_tools,
        messages=messages)
    
    dic_tools = {
        'read_file': filereader.read_file, 
        'search_web':websearch.search_web,
        'scrape_webpage':webscrapper.scrape_webpage
    }

    if agent_res['message']['content'] != '':
        res = agent_res["message"]["content"]
        print("🤖 > ", f"\x1b[1;30m{res}\x1b[0m")
        messages.append( {"role":"assistant", "content":res} )

    if "tool_calls" in agent_res["message"]:
        tools = deque(agent_res["message"]["tool_calls"])
        max_tools_calls = len(agent_res["message"]["tool_calls"]) + 3
        while tools and max_tools_calls > 0:
            tool = tools.popleft()
            t_name, t_inputs = tool["function"]["name"], tool["function"]["arguments"]
            if f := dic_tools.get(t_name):
                print("🔧 > ", f"\x1b[1;31m{t_name} -> Inputs: {t_inputs}\x1b[0m")
                messages.append( {"role":"user", "content":"use tool '"+t_name+"' with inputs: "+str(t_inputs)} )
                t_output = f(**tool["function"]["arguments"])
                max_tools_calls -= 1
                p = f'''
                    Now you will need to generate answer from the output of the tool.
                    Be research-oriented. If you cite something, use APA citation in your answer, link to it, and the page number if applicable.
                    You have access to these tools: {list_tools}, you must decide when to use those tools to further answer the researcher's message.
                    Summarize {t_output} to answer researcher's message {q}. You can answer it in details.
                    '''
                res = ollama.generate(model=llm, format=formatter.generate_format, prompt=q+". "+p)["response"]
                res_json = json.loads(res)
                print("🤖 > ", f"\x1b[1;30m{res_json['content']}\x1b[0m")
                messages.append({"role":"assistant", "content":res_json['content']})
                if 'tool_calls' in res_json and res_json['tool_calls'] != None:
                    tools.extend(res_json['tool_calls'])
            else:
                print("🤬 > ", f"\x1b[1;31m{t_name} -> NotFound\x1b[0m")