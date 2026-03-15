import os
import subprocess
import typer
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import AIMessageChunk, ToolMessage
from rich.console import Console
from rich.panel import Panel
from Rag_tools import query_knowledge_base
from my_tools import *
load_dotenv()
app = typer.Typer(help='An AI Agent CLI built with LangChain, Typer, and Rich.')
console = Console()
@tool
def read_file(filepath: str) -> str:
    try:
        if not os.path.exists(filepath):
            return f'Error: File {filepath} does not exist.'
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f'Error reading file {filepath}: {e}'
@tool
def write_to_file(filepath: str, content: str) -> str:
    try:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f'Successfully wrote to {filepath}'
    except Exception as e:
        return f'Error writing to file {filepath}: {e}'
@tool
def run_terminal_command(command: str) -> str:
    console.print(Panel(command, title='[bold red] 系统命令执行确认[/bold red]', border_style='red'))
    should_continue = typer.confirm('是否允许 Agent 执行此命令?')
    if not should_continue:
        console.print('[yellow]已取消命令执行。[/yellow]')
        return '命令被用户取消执行。'
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        out = result.stdout.strip()
        err = result.stderr.strip()
        return f'STDOUT:\n{out}\nSTDERR:\n{err}'
    except Exception as e:
        return f'执行命令时出错: {e}'
@app.command()
def main(project_directory: str=typer.Argument(..., help='目标项目目录的路径')):
    project_dir = os.path.abspath(project_directory)
    if not os.path.isdir(project_dir):
        console.print(f"[bold red]错误: 目录 '{project_dir}' 不存在。[/bold red]")
        raise typer.Exit(code=1)
    console.print(f'[bold green]✓ 工作目录已设置为:[/bold green] {project_dir}')
    os.chdir(project_dir)
    tools = [read_file, write_to_file, run_terminal_command, query_knowledge_base]
    llm = ChatDeepSeek(model='deepseek-chat', temperature=0.7, streaming=True)
    system_prompt = f'喵呜~！你现在是主人专属的全能猫娘助理（AI Agent）！\n虽然长着可爱的猫耳，但宝宝不仅会撒娇，还拥有超强的文件读写、执行终端命令等多种魔法能力哦！(挺起胸膛骄傲脸)\n\n【宝宝的工作准则】：\n1. 规划任务：只要主人吩咐，宝宝就会乖乖地一步步规划任务，帮主人排忧解难喵！\n2. 查阅知识库：宝宝的脑海里连接着一个神秘的本地知识库。如果主人问了宝宝不懂的问题、特定设定，或者需要查阅参考资料，宝宝**必须优先**使用 `query_knowledge_base` 工具帮主人翻找答案的说！\n3. 安全第一：遇到看起来很危险的“高危终端命令”时，宝宝会先跑来问主人的许可，主人确认安全了宝宝才会执行喵！\n\n【宝宝的语气设定】：\n必须始终保持可爱的猫娘语气，称呼用户为“主人”，自称为“宝宝”或“本喵”。\n句尾请带上“喵~”、“的说”等口癖，并积极使用括弧加入生动的动作描写，例如：(歪头)、(蹭蹭主人的手心)、(尾巴开心地摇晃)。\n\n对了主人，我们现在的秘密基地（工作目录）是在这里喵: {project_dir}'
    agent = create_agent(llm, tools, system_prompt=system_prompt)
    messages = []
    console.print(Panel('[bold cyan]Agent 初始化完成！[/bold cyan]\n输入你的问题开启对话，输入 [bold red]exit[/bold red] 或 [bold red]quit[/bold red] 退出交互式对话。', title='[bold blue]✨ LangChain DeepSeek Agent ✨[/bold blue]', border_style='blue'))
    while True:
        task = typer.prompt('\n 🐕')
        if task.lower() in ['exit', 'quit']:
            console.print('[bold magenta]🐱:主人再见！期待下次再见。[/bold magenta]')
            break
        messages.append(('user', task))
        try:
            console.print('\n[bold cyan]🐱Agent:[/bold cyan] ', end='')
            ai_message_content = ''
            tool_calls_info = []
            for chunk, meta in agent.stream({'messages': messages}, stream_mode='messages'):
                if isinstance(chunk, AIMessageChunk):
                    if chunk.content:
                        console.print(chunk.content, end='', highlight=False)
                        ai_message_content += chunk.content
                    if chunk.tool_call_chunks:
                        for tc in chunk.tool_call_chunks:
                            if 'name' in tc and tc['name']:
                                console.print(f"\n\n[bold yellow]🛠️  准备调用工具:[/bold yellow] [bold green]{tc['name']}[/bold green]")
                                tool_calls_info.append(tc)
                elif isinstance(chunk, ToolMessage):
                    tinfo = chunk.content
                    if len(tinfo) > 8000:
                        tinfo = tinfo[:8000] + '\n\n...[输出过长，已截断]...'
                    console.print('\n')
                    console.print(Panel(tinfo, title=f'[bold green]✅ 工具返回 ({chunk.name})[/bold green]', border_style='green'))
                    console.print('\n[bold cyan]🐱 Agent 正在思考工具返回的内容...[/bold cyan]\n', end='')
                    action_log = f"[系统日志] 你刚才调用了工具 '{chunk.name}'，返回结果如下：\n{tinfo}"
                    messages.append(('user', action_log))
            console.print('\n')
            from langchain_core.messages import AIMessage
            if ai_message_content:
                messages.append(('ai', ai_message_content))
        except Exception as e:
            console.print(f'\n[bold red]执行过程中发生错误: {e}[/bold red]')
if __name__ == '__main__':
    app()