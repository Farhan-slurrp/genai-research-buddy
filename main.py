import ollama
import websearch
import webscrapper

llm = "qwen2.5"


prompt = '''
You are a research assistant with access to tools, you must decide when to use tools to answer the researcher's message.
Be as research-oriented as possible. If you cite something, use APA citation in your answer. 
''' 
messages = [{"role":"system", "content":prompt}]

while True:
    try:
        q = input('🦰 > ')
    except EOFError:
        break
    if q == "quit":
        break
    if q.strip() == "":
        continue
    messages.append( {"role":"user", "content":q} )
   
    agent_res = ollama.chat(
        model=llm,
        tools=[websearch.tool_search_web, webscrapper.tool_scrape_webpage],
        messages=messages)
    
    dic_tools = {'search_web':websearch.search_web, 'scrape_webpage':webscrapper.scrape_webpage}

    res = ''
    if "tool_calls" in agent_res["message"]:
        for tool in agent_res["message"]["tool_calls"]:
            t_name, t_inputs = tool["function"]["name"], tool["function"]["arguments"]
            if f := dic_tools.get(t_name):
                print('🔧 >', f"\x1b[1;31m{t_name} -> Inputs: {t_inputs}\x1b[0m")
                messages.append( {"role":"user", "content":"use tool '"+t_name+"' with inputs: "+str(t_inputs)} )
                t_output = f(**tool["function"]["arguments"])
                p = f'''
                    Summarize this to answer user question, the answer should be usable for research purpose: {t_output}.
                    Remember to consider the tools description.
                    '''
                res = ollama.generate(model=llm, prompt=q+". "+p)["response"]
            else:
                print('🤬 > ', f"\x1b[1;31m{t_name} -> NotFound\x1b[0m")

    if agent_res['message']['content'] != '':
        res = agent_res["message"]["content"]
     
    print("🤖 > ", f"\x1b[1;30m{res}\x1b[0m")
    messages.append( {"role":"assistant", "content":res} )