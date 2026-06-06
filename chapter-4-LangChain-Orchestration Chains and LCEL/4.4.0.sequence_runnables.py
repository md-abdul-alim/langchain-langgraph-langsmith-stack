from langchain_core.runnables import RunnableSequence, RunnableLambda

runnable1 = RunnableLambda(lambda x: x + 1)
runnable2 = RunnableLambda(lambda x: x * 2)

print("------Using RunnableSequence-----")

sequence1 = RunnableSequence(
    first=runnable1,
    # middle=[runnable3, runnable4],
    last=runnable2
)

result_1 = sequence1.invoke(3)
print(result_1)  # Output: 8

print("----- Using pipe() -----")

sequence2 = runnable1.pipe(runnable2)
result_2 = sequence2.invoke(3)
print(result_2)  # Output: 8

print("----- Using LCEL (|) -----")
sequence3 = runnable1 | runnable2
result_3 = sequence3.invoke(3)
print(result_3)  # Output: 8