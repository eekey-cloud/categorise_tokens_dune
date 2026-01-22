import requests
import json
import csv
import io

# Stablecoin token addresses with their symbols
STABLECOINS = [
    {'address': 'CASHx9KJUStyftLFWGvEVf59SGeG9sh5FfcnZMVPCASH', 'symbol': 'CASH'},
    {'address': '6FrrzDk5mQARGc1TDYoyVnSyRdds1t4PbtohCD6p3tgG', 'symbol': 'USX'},
    {'address': '3ThdFZQKM6kRyVGLG48kaPg5TRMhYMKY1iCRa9xop1WC', 'symbol': 'eUSX'},
    {'address': 'USD1ttGY1N17NEEHLmELoaybftRBUSErhqYiQzvEmuB', 'symbol': 'USD1'},
    {'address': '5YMkXAYccHSGnHn9nob9xEvv6Pvka9DZWH7nTbotTu9E', 'symbol': 'hyUSD'},
    {'address': 'AvZZF1YaZDziPY2RCK4oJrRVrbN3mTD9NL24hPeaZeUj', 'symbol': 'syrupUSDC'},
    {'address': 'AUSD1jCcCyPLybk1YnvPWsHQSrZ46dxwoMniN4N2UEB9', 'symbol': 'AUSD'},
    {'address': 'GyWgeqpy5GueU2YbkE8xqUeVEokCMMCEeUrfbtMw6phr', 'symbol': 'BUIDL'},
    {'address': '2u1tszSeqZ3qBWF3uNGPFc8TzMk2tdiwknnRMWGWjGWH', 'symbol': 'USDG'},
    {'address': '9fvHrYNw1A8Evpcj7X2yy4k4fT7nNHcA9L6UsamNHAif', 'symbol': 'jlUSDG'},
    {'address': 'susdabGDNbhrnCa6ncrYo81u4s9GM8ecK2UwMyZiq4X', 'symbol': 'sUSD'},
    {'address': 'USDSwr9ApdHk5bvJKMjzff41FfuX8bSxdKcR81vTwcA', 'symbol': 'USDS'},
    {'address': 'j14XLJZSVMcUYpAfajdZRpnfHUpJieZHS4aPektLWvh', 'symbol': 'jlUSDS'},
    {'address': 'A1KLoBrKBde8Ty9qtNQUtq3C2ortoC3u7twggz7sEto6', 'symbol': 'USDY'},
    {'address': 'DEkqHyPN7GMRJ5cArtQFAWefqbZb33Hyf6s5iCwjEonT', 'symbol': 'USDe'},
    {'address': 'Eh6XEPhSwoLv5wFApukmnaVSHQ6sAnoD9BmgmwQoN2sN', 'symbol': 'sUSDe'},
    {'address': 'HzwqbKZw8HxMN6bF2yFZNrht3c2iXXzpKcFu7uBEDKtr', 'symbol': 'EURC'},
    {'address': '2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo', 'symbol': 'pyUSD'},
    {'address': '9zNQRsGLjNKwCUU5Gq5LR8beUCPzQMVMqKAi3SSZh54u', 'symbol': 'FDUSD'},
    {'address': 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB', 'symbol': 'USDT'},
    {'address': 'Cmn4v2wipYV41dkakDvCgFJpxhtaaKt11NyWV8pjSE8A', 'symbol': 'jlUSDT'},
    {'address': 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v', 'symbol': 'USDC'},
    {'address': '9BEcn9aPEmhSPbPQeFGjidRiEKki46fVQDyPpSQXPA2D', 'symbol': 'jlUSDC'},
    {'address': 'JuprjznTrTSp2UFa3ZBUFgwdAmtZCq4MQCwysN55USD', 'symbol': 'JupUSDC'},
    {'address': 'HVbpJAQGNpkgBaYBZQBR1t7yFdvaYVp2vCQQfKKEN4tM', 'symbol': 'USDP'},
    {'address': 'USDH1SM1ojwWUga67PGrgFWUHibbjqMvuMaDkRJTgkX', 'symbol': 'USDH'},
    {'address': 'GzX1ireZDU865FiMaKrdVB1H6AE8LAqWYCg6chrMrfBw', 'symbol': 'frxUSD'},
]

def get_stablecoin_data():
    """
    Return the hardcoded stablecoin list
    """
    return STABLECOINS

def convert_to_csv(stablecoin_data):
    """
    Convert list of stablecoins to CSV format string
    """
    if not stablecoin_data:
        return None

    output = io.StringIO()
    fieldnames = ['address', 'symbol']
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()
    for token in stablecoin_data:
        writer.writerow(token)

    csv_data = output.getvalue()
    output.close()

    return csv_data

def upload_to_dune(csv_data, api_key):
    """
    Upload CSV data to Dune Analytics
    """
    url = "https://api.dune.com/api/v1/uploads/csv"

    payload = {
        "data": csv_data,
        "description": "Stablecoin tokens data from Jupiter API",
        "table_name": "stablecoin_tokens",
        "is_private": False
    }

    headers = {
        "X-DUNE-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print("Successfully uploaded to Dune!")
        print(response.text)
        return True
    except Exception as e:
        print(f"Error uploading to Dune: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

def main():
    # Get stablecoin data
    stablecoin_data = get_stablecoin_data()

    if not stablecoin_data:
        print("No stablecoin data found.")
        return

    # Save as JSON for reference
    with open('stablecoin_output.json', 'w') as f:
        json.dump(stablecoin_data, f, indent=2)

    print(f"Found {len(stablecoin_data)} stablecoins")
    print(json.dumps(stablecoin_data, indent=2))

    # Convert to CSV
    csv_data = convert_to_csv(stablecoin_data)

    if csv_data:
        # Save CSV locally for reference
        with open('stablecoin_output.csv', 'w') as f:
            f.write(csv_data)
        print("\nCSV file created successfully")

        # Upload to Dune
        api_key = 'l2izTVbLIk5N5QRS4UQRNC0UdvmXDXTh'
        upload_to_dune(csv_data, api_key)

if __name__ == "__main__":
    main()
