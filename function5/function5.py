

# Final Result
final_Result={'eval_loss': 2.7519428730010986, 'eval_accuracy': 0.4074074074074074, 'eval_f1': 0.407631874298541,
'eval_precision': 0.4388888888888889, 'eval_recall': 0.4074074074074074, 'eval_runtime': 0.1112,
'eval_samples_per_second': 242.863, 'eval_steps_per_second': 17.99, 'epoch': 80.0}

#But if we accept some small error, for example we consider that predict AAA to AA is acceptable.
# Here, we think that it increases half accuracy in if prediction's error is adjacent,
# we will get a more reasonable way to evaluate the model eval_accuracy: 0.6296296296296297
adjusted_eval_accuracy = 0.6296296296296297