import oci
from datetime import datetime

from oci.config import from_file
config = from_file(profile_name="CDSLAB_ASH")

#core_client = oci.core.ComputeClient(config)
boot_volume_client = oci.core.BlockstorageClient(config)
identity_client = oci.identity.IdentityClient(config)

list_availability_domains_response = identity_client.list_availability_domains(
    compartment_id=config['tenancy']
)

list_compartments_response = identity_client.list_compartments(
       compartment_id=config['tenancy'],
       lifecycle_state="ACTIVE")

ad_list=[]
cmp_list=[]


for ad in range(len(list_availability_domains_response.data)):
  ad_list.append(list_availability_domains_response.data[ad].name)

for cmp in range(len(list_compartments_response.data)):
  cmp_list.append(list_compartments_response.data[cmp].id)

# Adding columns for boot volume name and created time

print("===============================================================================")
print("  BootVoumeName    ---------->    State        ----------->   Created On       ")
print("===============================================================================")


# Get a list of all boot volumes from compartments

for i,j in [(i,j) for i in cmp_list for j in ad_list]:
   boot_volumes=boot_volume_client.list_boot_volumes(
	compartment_id=i,
	availability_domain=j
   )
   if len(boot_volumes.data) !=0: 
   	for bt in range(len(boot_volumes.data)):
		   print(boot_volumes.data[bt].display_name + "          " + boot_volumes.data[bt].lifecycle_state + "         " + str((boot_volumes.data[bt].time_created).strftime("%Y-%m-%d %H:%M:%S")))

