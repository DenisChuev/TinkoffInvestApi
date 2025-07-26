from tinkoff.invest import OperationType, MoneyValue, OperationsResponse
import datetime


def get_operation_payment(payment: MoneyValue):
    result = 0.0
    result += payment.units

    if payment.nano < 0:
        result += payment.nano / 1000000000

    return result


def print_result(operations: OperationsResponse.operations, current_portfolio: MoneyValue):
    track_fee = 0.0
    broker_fee = 0.0
    money_input = 0.0
    money_output = 0.0
    current_amount = get_operation_payment(current_portfolio)

    for operation in operations:
        if operation.operation_type == OperationType.OPERATION_TYPE_TRACK_MFEE or operation.operation_type == OperationType.OPERATION_TYPE_TRACK_PFEE:
            track_fee += get_operation_payment(operation.payment)
            # print(operation)
            # print(track_fee)

        if operation.operation_type == OperationType.OPERATION_TYPE_BROKER_FEE:
            broker_fee += get_operation_payment(operation.payment)

        if operation.operation_type == OperationType.OPERATION_TYPE_INPUT:
            money_input += get_operation_payment(operation.payment)

        if operation.operation_type == OperationType.OPERATION_TYPE_OUTPUT:
            money_output += get_operation_payment(operation.payment)
        # print(operation)

    print(f"Current amount: {round(current_amount, 2)}")
    print(f"Track fee: {round(track_fee, 2)}")
    print(f"Broker fee: {round(broker_fee, 2)}")
    print(f"Money input: {round(money_input, 2)}")
    print(f"Money output: {round(money_output, 2)}")
    print(f"Result: {round(abs(money_output) - money_input + current_amount, 2)}")


def print_accounts():
    from tinkoff.invest import Client

    token = ''
    account_name = "ex стратегия"

    with Client(token) as client:
        accounts = client.users.get_accounts().accounts
        # print(accounts)

        strategy_account = None

        for account in accounts:
            print(f"Name: {account.name}, Created at: {account.opened_date.date()}")
            operations = client.operations.get_operations(account_id=account.id,
                                                          from_=datetime.datetime(2025, 1, 1, 0, 0, 0)).operations
            current_portfolio = client.operations.get_portfolio(account_id=account.id).total_amount_portfolio

            print_result(operations, current_portfolio)
            print()
            if account.name == account_name:
                strategy_account = account

        # operations = client.operations.get_operations(account_id=strategy_account.id).operations
        # print_result(operations)


if __name__ == '__main__':
    print_accounts()
