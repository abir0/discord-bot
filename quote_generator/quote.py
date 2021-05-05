import random


def generate_quote():
    list = [("Newton", "WTF Apple-chan, why did you fall upon my head!"),
            ("Einstein", "Gravity is curved baby."),
            ("Jett", "Wash dish."),
            ("Sova", "I'm da hunter. Shock dart.")]
    q = random.randint(0, len(list) - 1)
    return "\n\"{}\" \n\n ~ {}\n".format(list[q][1], list[q][0])


if __name__ == "__main__":
    print(generate_quote())
