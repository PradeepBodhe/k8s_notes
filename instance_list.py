import oci
from datetime import datetime

from oci.config import from_file
config = from_file(profile_name="CDSLAB_ASH")

instance_client = oci.core.ComputeClient(config)

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

# Adding columns for compute instance name, it's state and created time

print("==============================================================================")
print("  InstanceName   ----->   State   ----->   Created On                         ")
print("==============================================================================")

# Get a list of all compute instances from compartments

for i,j in [(i,j) for i in cmp_list for j in ad_list]:
   list_instances_response = instance_client.list_instances(
        limit=97,
	      compartment_id=i,
	      availability_domain=j,
        sort_order="ASC",
        lifecycle_state="RUNNING"
   )
   
   if len(list_instances_response.data) !=0: 
        for inst in range(len(list_instances_response.data)):
	     	     print(list_instances_response.data[inst].display_name + "           " + list_instances_response.data[inst].lifecycle_state + "           " + str((list_instances_response.data[inst].time_created).strftime("%Y-%m-%d %H:%M:%S")))
