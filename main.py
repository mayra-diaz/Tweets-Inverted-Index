from IndexHandler import IndexHandler

index = IndexHandler()

index.add('./test/')
print(index.analyze_query('Hola, Keiko es corrupta', 5))