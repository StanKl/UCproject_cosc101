"""Open, read, match transactions and print the results from two different files.
  Written for COSC480-20S1.
  Author: Stanislav Klevtsov.
  Date: 28 May 2020."""

import csv
import matplotlib.pyplot as plt

Line = "-"

def get_transactions(filename, sort_key):
    """This funtcion opens csv files and returns a sorted list of dictionaries
    where each entry in the list is a dictioary containing all feilds from the
    input file for the given line where each value is stored by the key of its field name"""
   
    internal_file = open(filename, encoding="utf8")
    transactions = []      
    csv_file = csv.DictReader(internal_file)
    for line in csv_file:
        #if condition
        transactions.append(line)
        
    transactions.sort(key=lambda x : x[sort_key] ) #sorts the file by the given sort_key field
    
    return transactions


def main():
    """main function that defines parameters names, creates several lists,
    matches transactions, locates these in approriate lists and prints the results"""
    
    internal_filename = "internal.csv" #data from the system
    internal_key = 'Bank Payment ID'
    internal_amount = 'Amount'
   
    external_filename = "external.csv" #data from the bank
    external_key = 'Account servicer reference'
	
	#get payments IDs
  
    internal_transactions = get_transactions(internal_filename, internal_key)
    external_transactions = get_transactions(external_filename, external_key)
    
    index_internal = 0  #index of current internal entry
    index_external = 0  #index of current external entry
    size_internal = len(internal_transactions) 
    size_external = len(external_transactions)
    standard_size = len('201910071196318274-158963569')
	
	#create list for different matching types (these types are
	#described in the document how to use the program. 
    
    no_id = []
    no_id_amount = 0
    diff_standard = []
    diff_standard_amount = 0
    LHV_online = []
    LHV_online_amount = 0
    duplicated = []
    duplicated_amount = 0 
    not_matched = []
    not_matched_amount = 0
    matched = []
    matched_amount = 0
    
    #Main comparison loop
    #while not at end of internal list and not at end of external
	#guarantees that the program finishes matching at the moment
	#when all keys in all lines (transactions) in the internal file have been checked.
    while index_internal < size_internal and index_external < size_external:
        
        previous = internal_transactions[index_internal-1]
        internal = internal_transactions[index_internal]
        if index_internal < size_internal-1:
            next_intenal = internal_transactions[index_internal+1]
        external = external_transactions[index_external]
        
        if internal[internal_key] == '':
            no_id.append(internal)
            no_id_amount += float(internal[internal_amount])
            index_internal += 1

        elif len(internal[internal_key]) != standard_size:
 
            if internal['Cash Flow Type'] == 'Deposit(LHV Online)':
                LHV_online.append(internal)
                LHV_online_amount += float(internal[internal_amount])
            else:
                diff_standard.append(internal)
                diff_standard_amount += float(internal[internal_amount])
            index_internal += 1
       
        elif previous[internal_key] == internal[internal_key] or internal[internal_key] == next_intenal[internal_key]:
            duplicated.append(internal)
            duplicated_amount += float(internal[internal_amount])
            index_internal += 1
        else:
            internal_change = False
            while not internal_change:
                if internal[internal_key] == external[external_key]:
                    matched.append(internal)
                    matched_amount += float(internal[internal_amount])
                    index_external += 1
                    index_internal += 1
                    internal_change = True
                elif internal[internal_key] < external[external_key]:
                    not_matched.append(internal)
                    not_matched_amount += float(internal[internal_amount])
                    index_internal += 1
                    internal_change = True
                else:
                    index_external += 1
                if not internal_change:
                    external = external_transactions[index_external]
    
    #If there are not yet checked transactions from the internal file
    if index_internal != size_internal-1:
        while index_internal < size_internal:
            #If the trnasaction id is non standard
            if len(internal[internal_key]) != standard_size:
                #If Cash Flow Type is Deposit(LHV Online)
                if internal['Cash Flow Type'] == 'Deposit(LHV Online)':
                    LHV_online.append(internal)
                    LHV_online_amount += float(internal[internal_amount])
                else:
                    diff_standard.append(internal)
                    diff_standard_amount += float(internal[internal_amount])
                index_internal += 1
            else:
                #Not matched
                not_matched.append(internal)
                not_matched_amount += float(internal[internal_amount])
                index_internal += 1            
    print(60 * Line)
    print('Completely matched transactions: {}, {} euros'.format(len(matched), matched_amount))            
    print('Transactions without ID: {}, {} euros'.format(len(no_id), no_id_amount))
    #print(no_id, '\n\n')
    print('Transactions with another standard of ID: {}, {} euros'.format(len(diff_standard), diff_standard_amount)) 
    #print('diff\n', diff_standard, '\n')
    print('Banklink transactions: {}, {} euros'.format(len(LHV_online), LHV_online_amount)) 
    #print('LHV online\n', LHV_online, '\n')
    print('Duplicated transactions: {}, {} euros'.format(len(duplicated), duplicated_amount))
    #print('dup\n', duplicated, '\n')
    print('Not matched transactions: {}, {} euros'.format(len(not_matched), not_matched_amount)) 
    #print('not matched\n', not_matched, '\n')
    print(60 * Line)
    
    y_data = [len(no_id), len(diff_standard), len(LHV_online), len(duplicated), len(not_matched)]
    names = ('No_id', 'Diff_standard', 'LHV_online', 'Duplicated', 'Not_matched')
    num_names = len(names)
    plt.bar(range(num_names), y_data)
    plt.title("Unmatched transactions")
    plt.xlabel("Type of error")
    plt.ylabel("Number of transactions")
    xtick_positions = []
    for i in range (num_names):
        xtick_positions.append(i)
    plt.xticks(xtick_positions, names)
    plt.show()
    
main()
