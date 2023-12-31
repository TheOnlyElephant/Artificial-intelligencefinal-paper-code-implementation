import random

# 定义问题场景
classroom_count = 10
timeslot_count = 6
course_count = 28

class Particle:
    def __init__(self, num_courses):
        self.position = [(random.randint(0, classroom_count-1), random.randint(0, timeslot_count-1)) for _ in range(num_courses)]
        self.velocity = [(0, 0) for _ in range(num_courses)]
        self.best_position = self.position
        self.fitness = 0

def fitness(schedule):
    used_slots = set()
    for course in schedule:
        slot = (course[0], course[1])
        if slot in used_slots:
            return 0  # 时间冲突，适应度为0
        used_slots.add(slot)
    return len(used_slots) / (classroom_count * timeslot_count)  # 教室利用率

def update_velocity(particle, global_best_position, inertia_weight, cognitive_weight, social_weight):
    for i in range(len(particle.velocity)):
        r1, r2 = random.random(), random.random()
        cognitive_component = [x - y for x, y in zip(particle.best_position[i], particle.position[i])]
        social_component = [x - y for x, y in zip(global_best_position[i], particle.position[i])]
        particle.velocity[i] = (
            inertia_weight * particle.velocity[i][0] + 
            cognitive_weight * r1 * cognitive_component[0] + 
            social_weight * r2 * social_component[0],
            inertia_weight * particle.velocity[i][1] + 
            cognitive_weight * r1 * cognitive_component[1] + 
            social_weight * r2 * social_component[1]
        )

def update_position(particle):
    for i in range(len(particle.position)):
        new_position = (
            max(0, min(classroom_count-1, particle.position[i][0] + round(particle.velocity[i][0]))),
            max(0, min(timeslot_count-1, particle.position[i][1] + round(particle.velocity[i][1])))
        )
        particle.position[i] = new_position

def pso_algorithm(num_particles, num_iterations, inertia_weight, cognitive_weight, social_weight):
    particles = [Particle(course_count) for _ in range(num_particles)]
    global_best_position = particles[0].position

    for iteration in range(num_iterations):
        for particle in particles:
            particle.fitness = fitness(particle.position)
            if particle.fitness > fitness(particle.best_position):
                particle.best_position = particle.position
            if particle.fitness > fitness(global_best_position):
                global_best_position = particle.position

        for particle in particles:
            update_velocity(particle, global_best_position, inertia_weight, cognitive_weight, social_weight)
            update_position(particle)

    return global_best_position, fitness(global_best_position)

# 参数设置
num_particles = 100
num_iterations = 300
inertia_weight = 0.8
cognitive_weight = 1.5
social_weight = 1.5

# 运行粒子群优化算法
best_schedule, best_fitness = pso_algorithm(num_particles, num_iterations, inertia_weight, cognitive_weight, social_weight)

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
