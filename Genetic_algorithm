import random

# 定义问题场景
classroom_count = 10
timeslot_count = 6
course_count = 28

# 生成初始种群
def generate_initial_population(population_size):
    population = []
    for _ in range(population_size):
        schedule = []
        while len(set(schedule)) < course_count:
            schedule.append((random.randint(0, classroom_count-1), random.randint(0, timeslot_count-1)))
        population.append(schedule)
    return population

# 计算适应度（教室利用率）
def fitness(schedule):
    used_slots = set()
    for course in schedule:
        slot = (course[0], course[1])
        if slot in used_slots:
            return 0  # 时间冲突，适应度为0
        used_slots.add(slot)
    return len(used_slots) / (classroom_count * timeslot_count)  # 教室利用率

# 选择操作
def selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:
        return random.choices(population, k=len(population))
    probabilities = [score / total_fitness for score in fitness_scores]
    return random.choices(population, weights=probabilities, k=len(population))

# 交叉操作
def crossover(parent1, parent2):
    crossover_point = random.randint(1, course_count - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# 变异操作
def mutation(child):
    mutated_child = child.copy()
    mutation_point = random.randint(0, course_count - 1)
    mutated_child[mutation_point] = (random.randint(0, classroom_count-1), random.randint(0, timeslot_count-1))
    return mutated_child

# 遗传算法主函数
def genetic_algorithm(population_size, generations):
    population = generate_initial_population(population_size)
    
    for generation in range(generations):
        fitness_scores = [fitness(schedule) for schedule in population]
        
        # 选择
        selected_population = selection(population, fitness_scores)
        
        # 交叉
        new_population = []
        for i in range(0, len(selected_population), 2):
            parent1, parent2 = selected_population[i], selected_population[i + 1]
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([child1, child2])
        
        # 变异
        new_population = [mutation(child) if random.random() < mutation_rate else child for child in new_population]
        
        population = new_population
    
    # 选出最优解
    best_schedule = max(population, key=fitness)
    best_fitness = fitness(best_schedule)
    
    return best_schedule, best_fitness


# 参数设置
population_size = 350
generations = 10000
mutation_rate = 0.3

# 运行遗传算法
best_schedule, best_fitness = genetic_algorithm(population_size, generations)

# 输出结果
print("最优教室安排方案：", best_schedule)
print("最优教室利用率：", best_fitness)


import pandas as pd
import matplotlib.pyplot as plt

# 将教室安排数据转换为 DataFrame
df = pd.DataFrame(best_schedule, columns=["教室编号", "时间槽编号"])

# 以时间槽为横坐标，教室为纵坐标，统计每个时间槽和教室的课程数量
table_data = pd.pivot_table(df, index="时间槽编号", columns="教室编号", aggfunc=len, fill_value=0)

# 创建表格
fig, ax = plt.subplots(figsize=(8, 6))
table = ax.table(cellText=table_data.values, colLabels=table_data.columns, rowLabels=table_data.index, cellLoc="center", loc="center", cellColours=None)

# 隐藏坐标轴
ax.axis("off")

# 显示表格
plt.show()

