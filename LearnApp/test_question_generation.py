from manual_together_ai_service import manual_together_ai

print("Manuel Together AI soru üretim testi...")

# Test 1: Matematik - Basit
print("\n=== Matematik - Basit ===")
questions = manual_together_ai.generate_question("Matematik", "Basit")
if questions:
    q = questions[0]
    print(f"Soru: {q['question']}")
    print(f"A) {q['options']['A']}")
    print(f"B) {q['options']['B']}")
    print(f"C) {q['options']['C']}")
    print(f"D) {q['options']['D']}")
    print(f"Doğru cevap: {q['correct_answer']}")
    print(f"Açıklama: {q['explanation']}")

# Test 2: Fizik - Orta  
print("\n=== Fizik - Orta ===")
questions2 = manual_together_ai.generate_question("Fizik", "Orta")
if questions2:
    q2 = questions2[0]
    print(f"Soru: {q2['question']}")
    print(f"A) {q2['options']['A']}")
    print(f"B) {q2['options']['B']}")
    print(f"C) {q2['options']['C']}")
    print(f"D) {q2['options']['D']}")
    print(f"Doğru cevap: {q2['correct_answer']}")
    print(f"Açıklama: {q2['explanation']}")

print("\nTest tamamlandı!")
