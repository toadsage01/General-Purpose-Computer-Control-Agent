import google.generativeai as genai

genai.configure(api_key="AIzaSyBvGOwYftTNXxhzM0ZewT7m480_k2Bf-SU")
for m in genai.list_models():
    print(m.name, m.supported_generation_methods)
