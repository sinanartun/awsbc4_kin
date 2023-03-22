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
last_data = None
kinesis_client = boto3.client(
    'kinesis',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['Token'],
    region_name='eu-central-1'
)



def main():

    symbol = 'BTCUSDT'

    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        kline.last_data = msg['k']
        if msg['k']['t'] != kline.last_time:
            print(msg['k'])
            kline.last_time = kline.last_data['t']
            data = str(kline.last_data['t']) + ","
            data += str(kline.last_data['o']) + ","
            data += str(kline.last_data['h']) + ","
            data += str(kline.last_data['l']) + ","
            data += str(kline.last_data['c']) + ","
            data += str(kline.last_data['v']) + ","
            data += str(kline.last_data['T'])

            print(data)
            data += str(kline.last_data['T']) + "," + ta.main()
            try:
                response = kinesis_client.put_record(StreamName='kline', Data=data, PartitionKey=str(kline.last_data['k']['t']))

            except ClientError:
                print("Couldn't put record in stream 'binance'")
                raise
            else:
                print(response)

    twm.start_kline_socket(callback=handle_socket_message, symbol=symbol, interval='1m')

    twm.join()


if __name__ == "__main__":
    main()
