"""
Runnables in Parallel

RunnableParallel
"""
from langchain_core.runnables import RunnableParallel, RunnableLambda

runnable1 = RunnableLambda(lambda input: str(input).upper())
runnable2 = RunnableLambda(lambda input: str(input).lower())

# Demo 1 - Passing a dictionary of Runnables to RunnableParallel
parallel_1 = RunnableParallel({
    "uppercase": runnable1,
    "lowercase": runnable2,
})

result_1 = parallel_1.invoke("Hello World")
print(result_1)

# Demo 2 - With Keyword Arguments
parallel_2 = RunnableParallel(
    uppercase=runnable1,
    lowercase=runnable2,
)

result_2 = parallel_2.invoke("Ich liebe Programmieren")
print(result_2)

# Demo 3.1 - LCEL
parallel_3 = parallel_1 | (lambda dict_int: dict_int["uppercase"] + " " + dict_int["lowercase"])
result_3 = parallel_3.invoke("Ich komme aus bangladesh")
print(result_3)

# Demo 3.2 - LCEL with Keyword Arguments
parallel_4 = {
    "uppercase": runnable1,
    "lowercase": runnable2,
} | RunnableLambda(lambda dict_int: dict_int["uppercase"] + " " + dict_int["lowercase"])
result_4 = parallel_4.invoke("Ich wohne in Rajshahi")
print(result_4)

chain = RunnableLambda(lambda input: str(input) + " Wow") | RunnableParallel({
    "uppercase": runnable1,
    "lowercase": runnable2,
})
result_5 = chain.invoke("Ich bin ein Student")
print(result_5)