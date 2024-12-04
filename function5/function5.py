

# Final Result
final_Result={'eval_loss': 3.2563703060150146, 'eval_accuracy': 0.5185185185185185,
'eval_f1': 0.4746031746031746, 'eval_precision': 0.5164609053497943,
'eval_recall': 0.5185185185185185, 'eval_runtime': 0.0957, 'eval_samples_per_second': 282.163,
'eval_steps_per_second': 20.901, 'epoch': 76.0}

#But if we accept some small error, for example we consider that predict AAA to AA is acceptable.
# Here, we think that it increases half accuracy in if prediction's error is adjacent,
# we will get a more reasonable way to evaluate the model eval_accuracy: 0.6296296296296297
adjusted_eval_accuracy = 0.6296296296296297