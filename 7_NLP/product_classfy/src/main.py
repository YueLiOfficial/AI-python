from argparse import ArgumentParser

if __name__ == "__main__":
    parse = ArgumentParser(usage="usage: main.py action")
    parse.add_argument("action", choices=["train", "predict", "evaluate", "run_server"])

    # 解析传入的参数
    action = parse.parse_args().action

    match action:
        case "train":
            from runner.train import train
            train()
        case "predict":
            from runner.predict import predict
            predict()
        case "evaluate":
            from runner.evaluate import evaluate
            evaluate()
        case "run_server":
            from web.app import run_server
            run_server()
