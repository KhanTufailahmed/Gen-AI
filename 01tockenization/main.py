import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")

text="Hello, I am Tufail"

tokens=enc.encode(text)

print(tokens)

tokens1=[13225, 11, 357, 939, 353, 1427, 663]

decode=enc.decode(tokens1)

print(decode)