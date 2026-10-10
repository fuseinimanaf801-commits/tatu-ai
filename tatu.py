# DAY 14 - TATU v1.0 FINAL AI
from datetime import datetime
import random

def find_streak(moods):
    if len(moods)==0: return 0,"none"
    max_streak=1; cur=1; best=moods[0]
    for i in range(1,len(moods)):
        if moods[i]==moods[i-1]:
            cur+=1
            if cur>max_streak: max_streak=cur; best=moods[i]
        else: cur=1
    return max_streak,best

def get_advice(mood, hp):
    happy_tips = ["Keep shining!", "Share your vibe!", "Make someone smile today!"]
    sad_tips = ["Take a walk, breathe", "Call someone you trust", "Small steps, you got this!"]
    tired_tips = ["Water + 20min nap = magic", "Stretch small", "Early bed tonight!"]
    if "fine" in mood or "happy" in mood or hp>=60:
        return random.choice(happy_tips)
    elif "sad" in mood:
        return random.choice(sad_tips)
    else:
        return random.choice(tired_tips)

def tatu_brain():
    now=datetime.now()
    today=now.strftime("%A %d %B %Y")
    time=now.strftime("%I:%M %p")
    print("=== TATU AI v1.0 - FINAL EDITION ===")
    print(today+" | "+time)
    print("Built by Manaf on Phone! 📱💻\n")
    name=input("Your name? ").strip()
    if name=="": name="manaf"
    print(f"\nWelcome {name}! This be TATU v1.0 - Full AI!\n")

    all_moods=[]; happy=0; sad=0; tired=0

    while True:
        mood=input("How you dey? fine/sad/tired/exit: ").lower().strip()
        if mood=="": continue
        if "exit" in mood or "bye" in mood:
            total=len(all_moods)
            if total==0: print("No data!"); break
            hp=int((happy/total)*100); sp=int((sad/total)*100); tp=int((tired/total)*100)
            streak_num,streak_mood=find_streak(all_moods)

            print(f"\n=== {name.upper()} FINAL v1.0 REPORT ===")
            print(f"Date: {today} {time}")
            print(f"Total chats: {total}")
            print(f"Moods: {all_moods}")
            print("\n--- BAR CHART ---")
            print(f"Happy [{happy}]: {'*' * happy} ({hp}%)")
            print(f"Sad [{sad}]: {'*' * sad} ({sp}%)")
            print(f"Tired [{tired}]: {'*' * tired} ({tp}%)")
            print(f"\nStreak: {streak_num}x {streak_mood}")

            # FINAL AI VERDICT + ADVICE
            final_advice = get_advice(streak_mood, hp)
            print("\n--- TATU AI VERDICT ---")
            if hp>=70:
                print("🌟 LEGEND STATUS! You be happiness machine!")
            elif hp>=50:
                print("⚖️ BALANCED BOSS! You dey manage life well!")
            else:
                print("💙 REAL ONE - Life get ups and downs, you still dey!")

            print(f"AI Advice: {final_advice}")

            final_diary = f"""
----- TATU v1.0 FINAL DIARY - COPY TO GITHUB ----
Date: {today} {time}
Coder: {name} - 14 Day Phone Challenge COMPLETE!
Moods: {all_moods}
Stats: Happy {hp}% | Sad {sp}% | Tired {tp}%
Streak: {streak_num}x {streak_mood}
AI Verdict: {'LEGEND' if hp>=70 else 'BALANCED' if hp>=50 else 'REAL ONE'}
Advice: {final_advice}
Project: TATU AI built 100% on phone - Programiz
Status: v1.0 GRADUATED! 🎓

"""
            print(final_diary)
            print("🎓 TATU v1.0 COMPLETE! 14 DAYS! YOU BE DEVELOPER NOW!")
            break

        all_moods.append(mood)
        if "fine" in mood or "good" in mood or "happy" in mood or "great" in mood:
            happy+=1
            print(f"TATU: Yooo {name}! {random.choice(['You dey glow!', 'Energy top!', 'Keep shining!'])}")
        elif "sad" in mood or "bad" in mood or "down" in mood:
            sad+=1
            print(f"TATU: {name}, {random.choice(['e go be fine', 'hold on king', 'I dey with you'])}")
        elif "tired" in mood or "sleep" in mood:
            tired+=1
            print(f"TATU: {name}, go rest small - {random.choice(['you deserve am', 'body need water', 'nap small'])}")
        else:
            print(f"TATU: I hear you {name}, tell me more")

tatu_brain()