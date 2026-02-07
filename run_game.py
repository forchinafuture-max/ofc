import subprocess

# 运行main.py并将输出重定向到文件
with open('game_output.txt', 'w', encoding='utf-8') as f:
    process = subprocess.Popen(
        ['python', 'main.py'],
        stdout=f,
        stderr=f,
        text=True
    )
    
    # 等待一段时间，然后终止进程
    try:
        process.wait(timeout=10)  # 等待10秒
    except subprocess.TimeoutExpired:
        process.terminate()
        print("游戏已启动并运行了10秒")
    else:
        print("游戏已运行完成")

print("游戏输出已保存到 game_output.txt")

# 读取并显示输出，处理编码问题
try:
    with open('game_output.txt', 'r', encoding='utf-8') as f:
        output = f.read()
        print("\n游戏输出:")
        print(output)
except UnicodeDecodeError:
    # 尝试使用其他编码
    try:
        with open('game_output.txt', 'r', encoding='gbk') as f:
            output = f.read()
            print("\n游戏输出 (GBK编码):")
            print(output)
    except Exception as e:
        print(f"读取文件失败: {e}")
        print("请直接查看 game_output.txt 文件获取详细输出")