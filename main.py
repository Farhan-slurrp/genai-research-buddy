from collections import deque
import json
import ollama
import websearch
import webscrapper
import formatter

llm = "qwen2.5"
list_tools = [websearch.tool_search_web, webscrapper.tool_scrape_webpage]


prompt = '''
You are a research assistant that will help researcher(s) with their research.

You MUST follow these guidelines in answering and helping the researcher:
1. You have access to tools, you must decide when to use tools to answer the researcher's message.
2. You can use multiple tools in answering the researcher input.
3. You can give details, try to help the researcher understand the whole concepts that you are saying.

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
    
    dic_tools = {'search_web':websearch.search_web, 'scrape_webpage':webscrapper.scrape_webpage}

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
                print('🔧 >', f"\x1b[1;31m{t_name} -> Inputs: {t_inputs}\x1b[0m")
                messages.append( {"role":"user", "content":"use tool '"+t_name+"' with inputs: "+str(t_inputs)} )
                t_output = f(**tool["function"]["arguments"])
                max_tools_calls -= 1
                p = f'''
                    Summarize this to answer user question, the answer should be usable for research purpose: {t_output}.
                    Be research-oriented. If you cite something, use APA citation in your answer, link to it, and the page number if applicable.

                    When summarizing, make sure to:
                        1. Consider the descriptions of the tools available and the initial system prompt.
                        2. If you return tool_calls, available tools are {list_tools}, but tool_calls can be empty
                    '''
                res = ollama.generate(model=llm, format=formatter.generate_format, prompt=q+". "+p)["response"]
                res_json = json.loads(res)
                print("🤖 > ", f"\x1b[1;30m{res_json['content']}\x1b[0m")
                messages.append({"role":"assistant", "content":res_json['content']})
                if res_json['tool_calls'] != None:
                    tools.extend(res_json['tool_calls'])
            else:
                print('🤬 > ', f"\x1b[1;31m{t_name} -> NotFound\x1b[0m")