import sys
import math

# Data Basis
stopword_list = ["about","all","along","also","although","among","and","any","anyone","anything","are","around","because","been","before","being","both","but","came","come","coming","could","did","each","else","every","for","from","get","getting","going","got","gotten","had","has","have","having","her","here","hers","him","his","how","however","into","its","like","may","most","next","now","only","our","out","particular","same","she","should","some","take","taken","taking","than","that","the","then","there","these","they","this","those","throughout","too","took","very","was","went","what","when","which","while","who","why","will","with","without","would","yes","yet","you","your",
"com","doc","edu","encyclopedia","fact","facts","free","home","htm","html","http","information","internet","net","new","news","official","page","pages","resource","resources","pdf","site","sites","usa","web","wikipedia","www","one","ones","two","three","four","five","six","seven","eight","nine","ten","tens","eleven","twelve","dozen","dozens","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety","hundred","hundreds","thousand","thousands","million","millions"]
category_list = {}
words_list = {}

# Reading Command Line
txt_name = sys.argv[1]
num_entry = int(sys.argv[2])

# Reading Inpput File
with open(txt_name) as f:
    entry = 0
    totalLst = []
    while(entry != num_entry):
        name = ""
        category = ""
        lst = []
        while(True):
            name = f.readline().rstrip("\n").rstrip(" ")
            if name:
                break
        category = f.readline().rstrip("\n").rstrip(" ")
        if category in category_list.keys():
            category_list[category] += 1
        else:
            category_list[category] = 1
            words_list[category] = {}
        while (True):
            words = f.readline().rstrip("\n").replace(","," ").replace("."," ").split(" ")
            for w in words:
                word = w.lower()
                if len(word)>2 and (word not in stopword_list):
                    if word not in lst:
                        lst.append(word)
                    if word not in totalLst:
                        totalLst.append(word)
            if words == [""]:
                break
        for item in lst:
            if item in words_list[category].keys():
                words_list[category][item]+=1
            else:
                words_list[category][item] = 1
        entry += 1
    
    for item in totalLst:
        for cate in category_list.keys():
            if item not in words_list[cate].keys():
                words_list[cate][item] = 0

# Learning Phase
    for item in category_list.keys():
        for word in words_list[item].keys():
            words_list[item][word] = words_list[item][word] / category_list[item]
        category_list[item] = category_list[item] / num_entry

    for item in category_list.keys():
        category_list[item] = (category_list[item]+0.1) / (1 + len(category_list)*0.1)
        for word in words_list[item].keys():
            words_list[item][word] = (words_list[item][word] + 0.1) / (1 + 2*0.1)

    for item in category_list.keys():
        category_list[item] = - math.log2(category_list[item])
        for word in words_list[item].keys():
            words_list[item][word] = - math.log2(words_list[item][word])


# Classification
    lines = f.readlines()
    status = "name"
    name = ""
    category = ""
    lst = []
    acc = "Wrong"
    num_acc = 0
    num_case = 0
    for line in lines:
        if line != "\n":
            if status == "name":
                name = line.rstrip("\n").rstrip(" ")
                status = "category"
            elif status == "category":
                category = line.rstrip("\n").rstrip(" ")
                status = "word"
            else:
                words = line.rstrip("\n").replace(","," ").replace("."," ").split(" ")
                for w in words:
                    word = w.lower()
                    if category in category_list.keys():
                        if len(word)>2 and (word not in stopword_list) and (word in words_list[category].keys()) and (word not in lst):
                            lst.append(word)
        if (line=="\n" and status == "word") or line == lines[-1]:
            status = "name"
            predict = {}
            for item in category_list.keys():
                value = category_list[item]
                for word in lst:
                    if word in words_list[item].keys():
                        value += words_list[item][word]
                predict[item] = value
            prediction = min(predict,key=predict.get)
            total = 0
            mean = predict[prediction]
            for item in predict.keys():
                predict[item] = math.pow(2,mean-predict[item])
                total += predict[item]
            for item in predict.keys():
                predict[item] = round(predict[item] / total,2)
            if prediction == category:
                acc = "Right"
                num_acc+=1
            print(name,"Prediction:",prediction,acc)
            print(predict)
            num_case+=1

            # Data clearance
            name = ""
            category = ""
            lst = []
            acc = "Wrong"

    print("Overall accuracy:",num_acc,"out of",num_case,"=","{:.2f}".format(num_acc/num_case))