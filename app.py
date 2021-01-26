#!/usr/bin/env python3

import csv
import sys


class Mapper:
    """This instance makes a correspondance between 2 csv files
    it takes the column from a first csv and map columns to a second csv"""
    def __init__(self, csv_from, csv_to, mapper=None):
        self.csv_from = csv_from
        self.csv_to = csv_to
        self.mapper = mapper

    def create_mapper(self, ):
        csv_from_header = read_file(self.csv_from, line_numbers=0) # get the file header
        csv_to_header = read_file(self.csv_to, line_numbers=0) # get the file header
        compare_columns_headers(csv_from_header, csv_to_header)

        while True:
            try:
                print('Press "q" to exit, "p" to print headers status')
                map_pair = input('Enter column map pair(from to)[1 2] >>')
                if map_pair in ['q', 'Q', 'exit']:
                    print(self.mapper)
                    return self.mapper

                elif map_pair in ['p', 'P', 'print']:
                    compare_columns_headers(csv_from_header, csv_to_header, self.mapper)
                    continue

                result = map_pair.split(' ')
                results = []
                for result1 in result:
                    results.append(int(result1))
                #TODO: add an error handling for not int values


                if len(results) != 2:
                    print('Error, need two values separated by space')
                if type(results[0]) == int and type(results[1]) == int:
                    if self.mapper == None:
                        self.mapper = {}

                    if results[0] in self.mapper.keys():
                        self.mapper[results[0]] = results[1]
                    else:
                        self.mapper[results[0]] = results[1] #TODO: useless at the moment

                else:
                    print('Error, pair should be int type separated by space, not: %s %s' %(type(results[0]), type(results[1])))



            except KeyboardInterrupt:
                print('Interrupted')
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)

                print('map: ', self.mapper)
        return self.mapper

    def save_file(self, filename):
        csv_to_header = read_file(self.csv_to, line_numbers=0)
        csv_from_header = read_file(self.csv_from, line_numbers=0)

        self.mapper = dict(sorted(self.mapper.items(), key=lambda item: item[1])) # sort mapper (need python 3.7 and more)

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(csv_to_header)
            first_line_passed = False

            for line1 in read_file(self.csv_from, line_numbers=None):
                if first_line_passed == False:
                    first_line_passed = True
                    continue

                output_line = [''] * len(csv_to_header) # Create an output list of len equal to output header length
                
                for key in self.mapper.keys(): # populate the values based on mapper
                    output_line[self.mapper[key]] = line1[key]
                
                writer.writerow(output_line)

        return filename


def compare_columns_headers(header1, header2, mapper={}):
    """This function compares 2 headers vertically (print them)
    """
    longest_header1 = len(max(header1, key=len))
    longest_header2 = len(max(header2, key=len))
    headers = [header1, header2]
    print('headers', headers)
    table_height = len(max(headers, key=len)) # find the maximum header length
    print('table_height', table_height)
    display_content1 = 'Header 1'
    display_content2 = 'Header 2'
    print(longest_header1)
    max_number_len = len(str(table_height))

    # print(f'{display_content1:^{longest_header1}}') 
    #, " | ", f'\n{display_content2:^{longest_header2}}')
    print(("{0:>"+str(longest_header1)+"}").format("header1") + "  " + ("{0:>"+str(longest_header2)+"}").format("header2"))
    for i in range(table_height):
        #print(i)
        print_str = ''
        if i < (len(header1)):
            if header1[i]:
                #print('header1[i]', header1[i])
                print_str += f'{i:^{max_number_len+1}}'
                if i in mapper.keys():
                    print_str += "\033[4m"
                    print_str += f'{header1[i]:^{longest_header1}}'
                    print_str += "\033[0m"
                else:
                    print_str += f'{header1[i]:^{longest_header1}}'

        else: 
            # print_str += ("{0:>"+str(longest_header1+2)+"}").format(" None ")
            print_str += f'{"":^{max_number_len+1}}' + f'{"":^{longest_header1}}'

        print_str += " | "
        if i < (len(header2)):
            if header2[i]:
                print_str += f'{i:^{max_number_len+1}}' 
                if i in mapper.values():
                    print_str += "\033[4m"
                    print_str += f'{header2[i]:^{longest_header2}}'
                    print_str += "\033[0m" 
                else:
                    print_str += f'{header2[i]:^{longest_header2}}'
        else:
            # print_str += ("{0:>"+str(longest_header2+2)+"}").format(" None ")
            print_str += f'{"":^{max_number_len+1}}' + f'{"":^{longest_header2}}'
        print(print_str)


        # else:
        # print((str(i+1)+"{0:>"+str(longest_header1)+"}").format(header1[i]) + "  " + (str(i+1)+"{0:>"+str(longest_header2)+"}").format(header2[i]))



def convert_contact(from_file, to_file, mapper):
    pass

def read_file(filename, line_numbers=None):
    """takes a filename and return a list of lines,
    lines returned are either all if line_number == None
    or filtered based on line_numbers (either list or int)
    """

    with open(filename, 'r', encoding="latin-1") as file:
        csv_reader = list(csv.reader(file, delimiter=',')) # TODO: could be more efficient for big file, not to open the complete file at once.

    if line_numbers == None:
        return csv_reader
    elif type(line_numbers) == int:
        return csv_reader[line_numbers]
    elif type(line_numbers) == list:
        return [csv_reader[i] for i in line_numbers]
    else: 
        print('lines_numbers should be int or list, not %s' %type(line_numbers))

def update_field(csv_from, csv_ref, csv_from_column_name, csv_ref_in_column_name, csv_ref_out_column_name, output_filename,):
    # replace a column name to an email.
    # in this example we take the output of deal_map and replace the contact name by the contact email.
    # Take a csv file, specify a reference csv file.
    # Take a column(csv_from_column_name) in csv_from, search value in csv_ref (csv_ref_in_column_name) and replace by (csv_ref_out_column_name)
    # then save to output_filename
    # this is to adjust some value that requires other refs. than the original export.

    lines = read_file(csv_from)
    ref_lines = read_file(csv_ref)

    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(lines[0])
        first_line_passed = False

        # Find column index
        csv_from_column_index = lines[0].index(csv_from_column_name)
        csv_ref_in_column_index = ref_lines[0].index(csv_ref_in_column_name)
        csv_ref_out_column_index = ref_lines[0].index(csv_ref_out_column_name)


        for line1 in lines:
            if first_line_passed == False:
                first_line_passed = True
                continue
            for line2 in ref_lines:

                if line1[csv_from_column_index] == line2[csv_ref_in_column_index]:
                    line1[csv_from_column_index] = line2[csv_ref_out_column_index]

            writer.writerow(line1)

def update_column(csv_from, csv_from_column_name, value, output_filename):
    """ Replace column value conditional to being empty (len less than 2)
    """

    lines = read_file(csv_from)
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(lines[0])
        first_line_passed = False
        csv_from_column_index = lines[0].index(csv_from_column_name)

        for line1 in lines:
            if first_line_passed == False:
                first_line_passed = True
                continue
            if len(line1[csv_from_column_index]) < 2:
                line1[csv_from_column_index] = value
            writer.writerow(line1)


def update_stage(csv_from, csv_from_column_name, mapper, output_filename):
    """will update the stage based on a mapper of the stages between the input and output"""
    lines = read_file(csv_from)
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(lines[0])
        first_line_passed = False
        csv_from_column_index = lines[0].index(csv_from_column_name)

        for line1 in lines:
            if first_line_passed == False:
                first_line_passed = True
                continue
            if line1[csv_from_column_index] in mapper.keys():
                line1[csv_from_column_index] = mapper[line1[csv_from_column_index]]
            writer.writerow(line1)



if __name__ == "__main__":
    # # Companies
    # # In zendesk Companies is the Contact with Is_company set to True
    # company_map1 = Mapper(csv_from='./data/ZendeskSell/contacts.0.csv', csv_to='./data/ZohoBigin/CompanySampleCsvFile.csv', mapper={4: 3, 5: 1, 6: 19, 10: 4, 15: 13, 16: 16, 18: 6, 19: 7, 20: 17, 23: 0, 25: 18, 29: 14, 31: 12, 34: 18, 36: 5, 37: 15})
    # company_map1.create_mapper()
    # company_map1.save_file('./CompanyOutput.csv')

    # # Contact
    # map1 = Mapper(csv_from='./data/ZendeskSell/contacts.0.csv', csv_to='./data/ZohoBigin/ContactSampleCsvFile.csv', mapper={0: 3, 1: 4, 4: 5, 6: 26, 7: 7, 8: 18, 9: 11, 10: 9, 15: 19, 16: 22, 17: 16, 20: 23, 23: 0, 25: 25, 29: 20, 31: 18, 32: 8, 34: 25, 37: 21})
    # map1.create_mapper()
    # map1.save_file('./contactoutput.csv')

    # # Deals
    # deal_map =  Mapper(csv_from='./data/ZendeskSell/deals.0.csv', csv_to='./data/ZohoBigin/DealSampleCsvFile.csv', mapper={0: 0, 1: 4, 3: 20, 5: 8, 9: 17, 10: 16, 11: 7, 12: 6, 14: 13, 20: 3, 22: 5, 25: 18})
    # deal_map.create_mapper()
    # deal_map.save_file('./DealOutput.csv')

    # #Correct the contact on deals
    # update_field(csv_from='./DealOutput.csv', 
    #             csv_ref='./data/ZendeskSell/contacts.0.csv', 
    #             csv_from_column_name='Contact ID', 
    #             csv_ref_in_column_name='id', 
    #             csv_ref_out_column_name='email', 
    #             output_filename='./DealOutputEmail.csv',
    #             )


    # # Update close date
    # update_column(csv_from='./DealOutputEmail.csv', csv_from_column_name='Closing Date', value='2021-01-01', output_filename='./DealOutputEmailCDate.csv')

    #update stage
    update_stage(csv_from='./DealOutputEmailCDate.csv', csv_from_column_name='Stage', mapper={'Unqualified': 'Closed Lost', 'Incomming': 'Qualification', 'Qualified': 'Needs Analysis', 'Quote': 'Proposal/Price Quote', 'Closure': 'Negotiation/Review', 'Won': 'Closed Won', 'Lost': 'Closed Lost'}, output_filename='./DealOutputEmailCDate2.csv')
