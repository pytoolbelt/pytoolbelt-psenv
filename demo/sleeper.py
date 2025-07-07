from time import sleep


def sleeper() -> None:
    for i in range(10):
        print("Sleeping for 1 second... time left:", 10 - i)
        sleep(1)
        if i == 5:
            return 0


if __name__ == "__main__":
    exit(sleeper())
    print("Done sleeping!")
