import subprocess


class Network:
    def __init__(self):
        self.__net_cat_categories = ['public', 'private']

    def __get_interface_data(self, interface_alias: str):
        alias_found = False
        index_found = False
        net_cat_found = False
        interface_index = 0
        network_category = ''
        result = subprocess.run(['powershell', '-Command', 'Get-NetConnectionProfile'], capture_output=True)
        lines = result.stdout.splitlines()
        lines = [str(x, 'UTF-8') for x in lines]
        for i in lines:
            if 'InterfaceAlias' in i:
                alias_val = i.split(':')[-1].strip()
                if alias_val.strip() == interface_alias:
                    alias_found = True
                    continue
            if 'InterfaceIndex' in i and alias_found:
                interface_index = int(i.split(':')[-1].strip())
                index_found = True
                continue
            if 'NetworkCategory' in i and alias_found and index_found:
                network_category = i.split(':')[-1].strip().lower()
                net_cat_found = True
                break
        if net_cat_found and network_category in self.__net_cat_categories:
            return interface_index, network_category
        return 0, ''

    def change_network_category(self, interface_alias: str, network_category_change_to: str):
        try:
            if network_category_change_to not in self.__net_cat_categories:
                return False
            interface_index, _ = self.__get_interface_data(interface_alias=interface_alias)
            if not interface_index:
                return False
            cmd_to_change = f'Set-NetConnectionProfile -InterfaceIndex {interface_index} -NetworkCategory '
            subprocess.run(['powershell', '-Command', cmd_to_change + self.__net_cat_categories[1 - self.__net_cat_categories.index(network_category_change_to)]], capture_output=True)
            subprocess.run(['powershell', '-Command', cmd_to_change + network_category_change_to], capture_output=True)
        except Exception as e:
            print(e)
            return False
        network_category = self.__get_interface_data(interface_alias=interface_alias)[-1]
        return network_category == network_category_change_to


if __name__ == '__main__':
    net = Network()
    res = net.change_network_category(interface_alias='Wi-Fi', network_category_change_to='private')
    print(res)
