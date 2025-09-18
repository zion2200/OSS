def read_data(filename):
    data = []
    # TODO) Read `filename` as a list of integers
    with open(filename, "r", encoding="utf-8") as table:
        rows = table.readlines()
     
    # header 안쓰는듯하니 일단 주석으로...    
    #head = rows[0].strip().split(",") # 머리글 떼내기
    #head = [col.lstrip("# ").strip() for col in head] # 머리글 "# " 기호 제거
    #data.append(head)
    
    for row in rows[1:]: # 내부 데이터 2차원 리스트 형태로 제작
        row = [int(col.strip()) for col in row.strip().split(",")]
        data.append(row)
    return data

def calc_weighted_average(data_2d, weight):
    # TODO) Calculate the weighted averages of each row of `data_2d`
    average = []
    
    for data in data_2d:
        score = 0
        
        for i in range(len(data)):
            score += data[i] * weight[i]
            
        average.append(score)
        
    return average

def analyze_data(data_1d):
    # TODO) Calculate summary statistics of the given `data_1d`
    # Note) Please don't use NumPy and other libraries. Do it yourself.
    mean = 0
    var = 0
    median = 0
    cal_mean = lambda lst : sum(lst) / len(lst)
    
    squared_data = []
    for i in data_1d:
        squared_data.append(pow(i,2))
        
    mean = cal_mean(data_1d) 
    var = cal_mean(squared_data) - pow(cal_mean(data_1d),2)
    median = sorted(data_1d)[len(data_1d)//2]
    
    return mean, var, median, min(data_1d), max(data_1d)

if __name__ == '__main__':
    data = read_data('data/class_score_en.csv')
    if data and len(data[0]) == 2: # Check 'data' is valid
        average = calc_weighted_average(data, [40/125, 60/100])
        # Write the analysis report as a markdown file
        with open('class_score_analysis.md', 'w') as report:
            report.write('### Individual Score\n\n')
            report.write('| Midterm | Final | Average |\n')
            report.write('| ------- | ----- | ----- |\n')
            for ((m_score, f_score), a_score) in zip(data, average):
                report.write(f'| {m_score} | {f_score} | {a_score:.3f} |\n')
            report.write('\n\n\n')

            report.write('### Examination Analysis\n')
            data_columns = {
                'Midterm': [m_score for m_score, _ in data],
                'Final'  : [f_score for _, f_score in data],
                'Average': average }
            for name, column in data_columns.items():
                mean, var, median, min_, max_ = analyze_data(column)
                report.write(f'* {name}\n')
                report.write(f'  * Mean: **{mean:.3f}**\n')
                report.write(f'  * Variance: {var:.3f}\n')
                report.write(f'  * Median: **{median:.3f}**\n')
                report.write(f'  * Min/Max: ({min_:.3f}, {max_:.3f})\n')