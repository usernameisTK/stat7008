"""
Result
"""
import numpy as np

def prediction_result():
    prediction = ['AA', 'AA', 'AA', 'AA', 'AAA', 'AA', 'AA', 'AA', 'AA', 'A', 'BBB', 'AAA', 'AA', 'AA'
        , 'A', 'AAA', 'AA', 'BBB', 'AA', 'AA', 'AAA', 'AA', 'BBB', 'AA', 'AA', 'BBB', 'AA']

    prediction = np.array(prediction)

    true = ['A', 'BB', 'AA', 'A', 'AA', 'AA', 'AA', 'BBB', 'BBB', 'A', 'BBB', 'AAA', 'BB', 'A'
        , 'AA', 'AAA', 'A', 'BBB', 'AA', 'A', 'AA', 'BBB', 'AAA', 'AA', 'AA', 'BBB', 'AA']

    true = np.array(true)

    # Final Result
    final_result={'eval_loss': 2.7519428730010986, 'eval_accuracy': 0.4074074074074074, 'eval_f1': 0.407631874298541,
    'eval_precision': 0.4388888888888889, 'eval_recall': 0.4074074074074074, 'eval_runtime': 0.1112,
    'eval_samples_per_second': 242.863, 'eval_steps_per_second': 17.99, 'epoch': 80.0}

    #But if we accept some small error, for example we consider that predict AAA to AA is acceptable.
    # Here, we think that it increases half accuracy in if prediction's error is adjacent,
    # we will get a more reasonable way to evaluate the model eval_accuracy: 0.6296296296296297
    adjusted_eval_accuracy = 0.6296296296296297

    return true, prediction, final_result, adjusted_eval_accuracy

def model_prediction():
    while True:
        print("\nPlease select an option:")
        print("1. Introduction of the model prediction")
        print("2. Get the result report of the BERT model prediction.")
        print("3. Quit")
        choice_m = int(input("Chatbot: Your choice (1/2/3): "))
        if choice_m == 1:
            print("Introduction of the model prediction:")
            print(
                "We collected 134 ESG annual report from the Internet. All of the ESG score of these company is collected on the website: https://www.msci.com/zh/esg-ratings/issuer.\n "
                "The ESG score range is: AAA, AA, A, BBB, BB, B, CCC, where AAA is the best. We wish to predict ESG score using related ESG annual report.\n"
                "Here, we firstly use library 'transformers' to conclude the report to a short article. Then we use BERT model to predict the ESG score.\n")
            choice_s = int(input("Please input 1 to find the prediction result."))
            if choice_s == 1:
                true, prediction, final_result, adjusted_eval_accuracy = prediction_result()
                print(f"True class in test data: \n{true}\n")
                print(f"Predicted class for the test data: \n {prediction}\n")
                print(f"Prediction result: {final_result}\n")
                print(f"Adjusted evaluation accuracy: {adjusted_eval_accuracy}\n")
            else:
                break
        elif choice_m == 2:
            true, prediction, final_result, adjusted_eval_accuracy = prediction_result()
            print(f"True class in test data: {true}\n")
            print(f"Predicted class for test data: {prediction}\n")
            print(f"Prediction result: {final_result}\n")
            print(f"Adjusted evaluation accuracy: {adjusted_eval_accuracy}\n")
        else:
            break