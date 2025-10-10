import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    midterm_range = np.array([0, 125])
    final_range = np.array([0, 100])

    # Load score data
    class_kr = np.loadtxt('data/class_score_kr.csv', delimiter=',')
    class_en = np.loadtxt('data/class_score_en.csv', delimiter=',')
    data = np.vstack((class_kr, class_en)) # [mid, final]

    # Estimate a line: final = slope * midterm + y_intercept
    # W*midterm + b = final
    # data: 94x2
    # w = 1x2
    # 적당한 init (자비에 init)
    line = [9, 9] # TODO) Find the best [slope, y_intercept] from 'data'
    w = line[0]
    b = line[1]
    
    # 학습 loop
    for epoch in range(10000):
        total_lossw = 0
        total_lossb = 0

        # eval
        for i in data:
            x = i[0]
            y = i[1]
            
            # loss 계산
            pred = w*x + b
            lossw = (pred-y) * x # scale
            lossb = pred-y             
            total_lossw += lossw
            total_lossb += lossb
        # calculate gradient
        gradientW = total_lossw / len(data)
        gradientB = total_lossb / len(data)
        
        # update
        w = w - 0.00001*gradientW
        b = b - 0.00001*gradientB
        print(f"epoch:{epoch}|lossW:{total_lossw}|lossb:{total_lossb}")
        
    line = [round(w,3), round(b,3)]
    print(line)
    # Predict scores
    final = lambda midterm: line[0] * midterm + line[1]
    while True:
        try:
            given = input('Q) Please input your midterm score (Enter or -1: exit)? ')
            if given == '' or float(given) < 0:
                break
            print(f'A) Your final score is expected to be {final(float(given)):.3f}.')
        except Exception as ex:
            print(f'Cannot answer the question. (message: {ex})')
            break

    # Plot scores and the estimated line
    plt.figure()
    plt.plot(data[:,0], data[:,1], 'r.', label='The given data')
    plt.plot(midterm_range, final(midterm_range), 'b-', label='Prediction')
    plt.xlabel('Midterm scores')
    plt.ylabel('Final scores')
    plt.xlim(midterm_range)
    plt.ylim(final_range)
    plt.grid()
    plt.legend()
    plt.show()
