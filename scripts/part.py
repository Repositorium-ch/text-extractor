from unstructured.partition.pdf import partition_pdf
elements = partition_pdf(filename="../data/zweispaltig.pdf")

for element in elements:
  print(element.text)
  # print(element.metadata.to_dict())
  print('\r\n')