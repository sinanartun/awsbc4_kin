import time
import boto3
import asyncio
import datetime
from binance import AsyncClient, BinanceSocketManager
from botocore.exceptions import ClientError
import get_credentials
from binance import ThreadedWebsocketManager
import kline
import ta

api_key = 'bXUPD49c3jXqEHKkbHvn7hrBNXz2zX0hQHyfVuR6Y8XNFn37teQRIIRjVmy303KC'
api_secret = 'jsIKSMC6znLU8u7gfh0FQ6Ho0Xa0oFzJ8qca5N5ic2GBgrLnWRNuyy1Ubski6Z2A'
last_time = 0
credentials = get_credentials.get()
kinesis_client = boto3.client(
    'kinesis',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['Token'],
    region_name='eu-north-1'
)


def main():
    symbol = 'BTCUSDT'

    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        if msg['k']['t'] != kline.last_time:
            kline.last_time = msg['k']['t']
            data = str(msg['k']['t']) + ","
            data += str(msg['k']['o']) + ","
            data += str(msg['k']['h']) + ","
            data += str(msg['k']['l']) + ","
            data += str(msg['k']['c']) + ","
            data += str(msg['k']['v']) + ","
            data += str(msg['k']['T']) + "," + ta.main()
            try:
                response = kinesis_client.put_record(StreamName='kline', Data=data, PartitionKey=str(msg['k']['t']))

            except ClientError:
                print("Couldn't put record in stream 'binance'")
                raise
            else:
                print(response)

    twm.start_kline_socket(callback=handle_socket_message, symbol=symbol, interval='1m')

    twm.join()


if __name__ == "__main__":
    main()
