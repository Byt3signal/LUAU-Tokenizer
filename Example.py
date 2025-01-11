from luau_tokenizer import tokenize_luau

code = '''
local function greet()
    print("Mars is cool!")
end

greet()
'''

tokenize_luau(code) #output Check ExampleOutput
