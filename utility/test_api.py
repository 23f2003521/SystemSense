from system_checks import (
    check_disk_encryption,
    check_os_update_status,
    check_antivirus_status,
    check_inactivity_sleep,
    gather_machine_info,
    gather_health_info
)

print("Disk Encryption:", check_disk_encryption())
print("OS Update:", check_os_update_status())
print("Antivirus:", check_antivirus_status())
print("Inactivity Sleep:", check_inactivity_sleep())
print("Machine Info:", gather_machine_info())
print("Health Info:", gather_health_info())