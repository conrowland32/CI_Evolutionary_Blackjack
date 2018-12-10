import matplotlib.pyplot as plt

if __name__ == "__main__":
    average_scores = []
    best_scores = []
    average_scores = []
    best_scores = []

    average_file = open("long/average.txt", 'r')
    average_scores = average_file.readlines()
    average_scores = [float(i.strip()) for i in average_scores]
    average_file.close()

    best_file = open("long/best.txt", 'r')
    best_scores = best_file.readlines()
    best_scores = [float(i.strip()) for i in best_scores]
    best_file.close()

    y = [j for j in range(len(average_scores))]
    average_player = [2000 * -0.15] * len(average_scores)
    optimal_player = [2000 * -0.005] * len(average_scores)

    plt.plot(y, average_scores, 'r-', label='Average')
    plt.plot(y, best_scores, 'b-', label='Best')
    plt.plot(y, average_player, 'k--', label='Avg Human')
    plt.plot(y, optimal_player, 'g--', label='Basic Strategy')
    plt.legend()
    plt.xlabel('Generation', fontdict={
               'fontweight': 'bold', 'fontsize': 'large'})
    plt.ylabel('Money Won/Lost',
               fontdict={'fontweight': 'bold', 'fontsize': 'large'})
    plt.grid(True)

    plt.show()
