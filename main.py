import re
import os
import json
import argparse
from collections import Counter


def process_log(log_file):
    methods_quantity_dict = {"TOTAL": 0,
                             "METHOD": {"POST": 0, "GET": 0, "DELETE": 0, "PUT": 0, "HEAD": 0, "OPTIONS": 0}}
    ip_list = []
    requests_list = []

    with open(log_file, 'r') as file:
        for line in file:
            ip = re.search(r"\d+\.\d+\.\d+\.\d+", line).group()
            ip_list.append(ip)
            method = re.search(r"POST|GET|PUT|DELETE|HEAD|OPTIONS", line).group()
            url = re.search(r"\"http.*?\"", line)
            duration = re.search(r'\d+$', line).group()
            date = re.search(r"\[\d.*?\]", line).group()

            methods_quantity_dict['TOTAL'] += 1
            methods_quantity_dict['METHOD'][method] += 1

            request_dict = {'method': method,
                            'url': None if url is None else url.group().strip("\""),
                            'ip': ip,
                            'duration': duration,
                            'date': date}

            requests_list.append(request_dict)

    count_ip = Counter(ip_list)
    quantity_ip_list = [ip for ip in count_ip.items()]
    sort_quantity_ip = sorted(quantity_ip_list, key=lambda x: x[1], reverse=True)[:3]

    top_ip_dict = {f'ip_{index + 1}': ip for index, (ip, _) in enumerate(sort_quantity_ip)}

    sorted_requests_list = sorted(requests_list, key=lambda x: int(x['duration']), reverse=True)[:3]

    report = {'count_requests': methods_quantity_dict['TOTAL'],
              'count_methods': methods_quantity_dict['METHOD'],
              'top_3_ip_address': top_ip_dict,
              'top_3_long_request': sorted_requests_list}

    with open("report.json", "w") as file:
        json.dump(report, file, indent=4)
        print(json.dumps(report, indent=4))


def main():
    parser = argparse.ArgumentParser(description="Process access.log")
    parser.add_argument(dest="log", action="store", help="Path to log file")
    args = parser.parse_args()

    log_file = args.log

    if log_file:
        if os.path.isfile(log_file):
            process_log(log_file)
        elif os.path.isdir(log_file):
            for file in os.listdir(log_file):
                if file.endswith(".log"):
                    process_log(os.path.join(log_file, file))
        else:
            print("Invalid path to log file")


if __name__ == '__main__':
    main()
