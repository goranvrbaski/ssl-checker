import sys
import ssl
import socket
import datetime
import logging
import argparse

console_logger = logging.StreamHandler(sys.stdout)
console_logger.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(console_logger)


def get_certificate_info(domain_name: str, port: int = 443) -> dict:
    """
    Extracts certificate info

    :param str domain_name: Domain name
    :param int port: Port number
    :return: Information about SSL certificate
    :rtype: dict
    """
    try:
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain_name)
        conn.settimeout(5.0)

        conn.connect((domain_name, port))
        ssl_info = conn.getpeercert()

        return ssl_info

    except socket.gaierror:
        logger.error(f"{domain_name} can't retrieve certificate info")


def get_days_left(certificate_info: dict) -> int:
    """
    Returns a number of days

    :param dict certificate_info: certificate_info
    :return: number of days
    :rtype: int
    """
    if 'notAfter' not in certificate_info.keys():
        exit(50)

    date = datetime.datetime.strptime(certificate_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
    expire_date = date - datetime.datetime.utcnow()

    return expire_date.days


def process_domains(domain_list: list, threshold: int) -> None:
    """
    Process domain list for expiration date

    :param list domain_list: List of domain names
    :param int threshold: Threshold days for comparing
    :return: None
    """
    for domain in domain_list:
        try:
            cert_info = get_certificate_info(domain)
            days = get_days_left(cert_info)

            if days <= threshold:
                logger.warning(f"{domain} expires in {days} days(s)")
            else:
                logger.info(f"{domain} expires in {days} days(s)")

        except AttributeError as ex:
            pass

        except Exception as ex:
            logger.error(f"Error occurred {ex}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check SSL certificate for expiration date')
    parser.add_argument('domains', type=str, action='append', help='domain names')
    parser.add_argument('-d', '--days', type=int, default=30, help='number of days')

    args = parser.parse_args()
    domains = args.domains[0].split(',')

    process_domains(domains, args.days)



