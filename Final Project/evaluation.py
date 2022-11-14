# The model output should be recorded in a dictionary with locations as the keys and the corresponding
# predicted seasons as the values; the answer key is recorded similarly with best seasons replacing the 
# predicted seasons. The adjusted accuracy and accuracy scores would be outputted to a text file.

def eval_w_adjustment (output, answerkey):
    score = 0
    adjusted_score = 0
    for i in output.values():
        if i == "spring":
            if answerkey[i] == "spring" or answerkey[i] == "fall":
                score += 1
                adjusted_score += 1
            if answerkey[i] == "summer" or answerkey[i] == "winter":
                adjusted_score += 0.5
        if i == "summer":
            if answerkey[i] == "summer":
                score += 1
                adjusted_score += 1
            if answerkey[i] == "fall" or answerkey[i] == "spring":
                adjusted_score += 0.5
        if i == "fall":
            if answerkey[i] == "spring" or answerkey[i] == "fall":
                score += 1
                adjusted_score += 1
            if answerkey[i] == "summer" or answerkey[i] == "winter":
                adjusted_score += 0.5
        if i == "winter":
            if answerkey[i] == "winter":
                score += 1
                adjusted_score += 1
            if answerkey[i] == "fall" or answerkey[i] == "spring":
                adjusted_score += 0.5

    outputf = open("evaluation.output", 'w')
    outputf.write("Accuracy = " + score/len(output) + "\n")
    outputf.write("Adjusted Accuracy = " + adjusted_score/len(output) )