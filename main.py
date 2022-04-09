import requests
import ast

def main():
    boards = ['sci','pol','g','his']
    for board in boards:get_last_scan_info(board)


def get_last_scan_info(board):
    print(board)
    b = False
    

    
    
    try:
        with open(f'last_op/last_op_{board}.txt', 'r') as f:last_op=f.read()
    except:
        with open(f'last_op/last_op_{board}.txt', 'w') as f:f.write()
    if last_op == '':last_op = 1
    try:
            r1 = str(requests.get(f'https://a.4cdn.org/{board}/archive.json').text)
    except:
        print('api not reachable')
        quit()


    list_of_ops=r1.replace(']','').replace('[','').split(',')

    for x in range(len(list_of_ops)-1,0,-1):
        if float(list_of_ops[x])==float(last_op):
            b=list_of_ops[x]
            list_of_ops=list_of_ops[x+1:]
            break



    if not b:b=list_of_ops[-1]
    print(b)
    with open(f'last_op/last_op_{board}.txt', 'w') as f:
        f.write(str(b))

    extension_list = ['.com','.org','.gov']

    l = read_journal_file()
    journal_list = sort_journals(l)
    
     

    paper_count = (link_extractor(list_of_ops,extension_list,board,journal_list))
    pop_list=(sorted(paper_count.items(), key =lambda kv:(kv[1], kv[0])))
    try:
        with open('dict.txt', 'r') as f:
            old_paper_count= ast.literal_eval(f.read())
            for key,value in paper_count.items():   
                old_paper_count[key]= old_paper_count.get(key,0)+1




    finally:
        with open('dict.txt', 'w') as f:f.write(str(paper_count))
    

def link_extractor(list_of_ops,extension_list,board,journal_list):
    paper_count = dict()
    match=0
    for i in list_of_ops:
        
        try:
            thread=str(requests.get(f'https://a.4cdn.org/{board}/thread/{i}.json').text)
        except:
            print('api not reachable')
            quit()
        
        indexes = kmp_index(extension_list,thread)

        for index in indexes:  


            list=(extract_web_address(thread,index))
            link=parse(str(list[0]))
            site=str(list[1])
            if link[-1]=='/':link = link[:-1]
            
            if journal_match(journal_list, site):
                if link[-1]=='/':link = link[:-1]
                paper_count[link]= paper_count.get(link,0)+1
                print(link)
                with open(f'journal_links/{board}_links.txt', 'a') as f:
                    f.write(link + '\n')
    return paper_count
    
def kmp_index(pattern_list, string):
    for pattern in pattern_list:
        table = kmp_preprocess(pattern)
        pattern_position = shift = 0
        matches = 0
    

        while shift<len(string)-pattern_position:
            while pattern_position<(len(pattern)):
                if string[shift+pattern_position]!=pattern[pattern_position]:
                    
                    shift+=1
                    pattern_position=table[pattern_position]
                elif pattern_position == len(pattern)-1:
                    
                    
                    yield shift + pattern_position - 3
                    
                    
                    shift+=1
                    pattern_position=table[pattern_position]
                else:
                    pattern_position+=1
                    
                if shift+pattern_position+1==len(string):break
            if shift+pattern_position+1==len(string):break




def kmp_preprocess(pattern):
    table = [0]*(len(pattern))
    
    for i in range(len(pattern)):
        for j in range(1,i):
            if pattern[j:i+1]==pattern[:i-j+1]:
                table[i]=i-j+1
                
                break

    return(table)

def parse(web_address):
    return web_address.replace('<wbr>','').replace("\\","")






def extract_web_address(thread,index):
    x=True
    for j in range(0,-200,-1):
        if thread[index+j-1]=='.':
            if x:
                k=j
                x=False
            if thread[index+j-4:index+j-1]=='www':
                j-=1
                break

        elif thread[index+j]=='/':break
        elif thread[index+j]=='"':break
        elif thread[index+j]==' ':break
        

    for h in range(200):
        if thread[index+h]==',':
            h-=1
            break
        elif thread[index+h]=='"':break
        elif thread[index+h]==';':break
        elif thread[index+h]=='<' and thread[index+h+1]!='w':break
        elif thread[index+h]==' ':break
    if x:
        k=j+1
    
    return [thread[index+j+1:index+h], thread[index+k:index]]#



def read_journal_file():
    with open('journals.txt', 'r') as f:
        journal_list = clean_list(f.read().split(','))

    return journal_list

def write_journal_file(journal_list):
    with open('journals.txt','w') as f:
        for journal in journal_list:
            f.write(journal+',')



def partition(start, end, array):
    pivot_index = start 
    pivot = array[pivot_index]
    while start < end:
        while start < len(array) and array[start] <= pivot:start += 1
        while array[end] > pivot:end -= 1
        if(start < end):array[start], array[end] = array[end], array[start]
    array[end], array[pivot_index] = array[pivot_index], array[end]
    return end

def quick_sort(start, end, array):
    if (start < end):
        p = partition(start, end, array)
        quick_sort(start, p - 1, array)
        quick_sort(p + 1, end, array)
          
def sort_journals(array):
    array = read_journal_file()
    start = 0
    end = len(array)-1
    quick_sort(start,end,array)
    write_journal_file(array)
    return array

def journal_match(journal_list, site):
    x = binary_search(journal_list,site, 0, len(journal_list)-1)
    if x ==-1:
        return False
     
    return True

def clean_list(list):
    x=0
    for i in range(len(list)):
        if list[i-x]=='':
            del list[i-x]
            x+=1
    return list

  


 
 
def binary_search(arr, x, l, r):
 
    
    if r >= l:
 
        mid = l + (r - l) // 2
 
   
        if arr[mid] == x:
            return mid
 
 
        elif arr[mid] > x:
            return binary_search(arr,x,l,mid-1)

        else:
            return binary_search(arr,x,mid+1,r)
 
    else:

        return -1
 
main()