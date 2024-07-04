from collections import defaultdict

def dfs(node, parent, balance, counter, adj, colors):
    # 更新当前路径的平衡状态
    balance += colors[node]
    if balance == 0:
        counter[0] += 1
    counter[0] += counter[1].get(balance, 0)
    counter[1][balance] = counter[1].get(balance, 0) + 1

    # 遍历每一个子节点，递归计算平衡路径
    for child in adj[node]:
        if child != parent:
            dfs(child, node, balance, counter, adj, colors)

    # 回溯时减少对应的平衡状态数量
    counter[1][balance] -= 1

def count_balanced_paths(n, colors_str, edges):
    adj = defaultdict(list)
    colors = [1 if c == 'R' else -1 for c in colors_str]

    for u, v in edges:
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)

    total_paths = 0
    visited = [False] * n

    for i in range(n):
        if not visited[i]:
            path_count = [0]
            seen_balances = defaultdict(int)
            dfs(i, -1, 0, path_count, adj, colors)
            total_paths += path_count[0]

            def mark_visited(v, parent):
                visited[v] = True
                for neighbor in adj[v]:
                    if neighbor != parent:
                        mark_visited(neighbor, v)

            mark_visited(i, -1)

    return total_paths

# 测试用例
n = 5
colors_str = "RRRBB"
edges = [(1, 2), (1, 3), (1, 4), (4, 5)]

# 调用函数计算路径
print(count_balanced_paths(n, colors_str, edges))
