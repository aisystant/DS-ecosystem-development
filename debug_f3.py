import sys
sys.path.append('ops')
from build_report import ReportGenerator

gen = ReportGenerator()
gen.scan_documents()  # Важно: сканируем документы!

docs_f3 = gen.by_family.get('F3', [])
print(f'F3 документы: {len(docs_f3)}')

for i, doc in enumerate(docs_f3[:3]):
    print(f'\nДокумент {i+1}: {doc.name}')
    print(f'Длина: {len(doc.body.split())} слов')
    print(f'Stub: {gen._is_stub_document(doc)}')
    print(f'Отвечает на вопрос: {gen._answers_main_question(doc, "Как работаем с внешним миром?")}')
    print(f'Содержание (первые 200 символов): {repr(doc.body[:200])}')