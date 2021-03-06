import os, sys

import argparse

import numpy as np

def convert_to_conll(npz_file, bpe_file, conll_file):
  output=np.load(npz_file)
  labels=output['labels']
  deps  =output['deps']
  
  f_conll=open(conll_file, 'w')
  
  idx=0
  for idx, bpe in enumerate( open(bpe_file, 'r') ):
    #print(idx, bpe.strip())
    words  = bpe.replace('@@', '').split()
    bpe_words = [ s.replace('@@', ' ') for s in bpe.split() ]
    bpe_word_len = np.array( [ len(s.split()) for s in bpe_words ] )
    #bpe_word_len[0] = 0 # Fix up first entry idx=0
    bpe_word_idx = np.cumsum(bpe_word_len)[:-2]  # Take off ending
    
    print(idx, bpe_words)
    #print(idx, bpe_word_idx, bpe_words)
    #print(idx, bpe_word_len, bpe_word_idx, bpe_words)
    
    labels_idx = labels[idx,:]
    deps_idx = deps[idx,:]
    
    # Ok, so now let's go through the indices and look at the values
    line_i=0
    for i in bpe_word_idx:
      line_i+=1
      
      label = labels_idx[i]
      dep = deps_idx[i]   # Ahh - but this is in bpe units ... translate to words...
      dep_word_idx = np.searchsorted(bpe_word_idx, dep, side='right')
     
      if dep!=dep_word_idx:
        print(i, label, dep, dep_word_idx)
      
      parent_id_str = str(dep_word_idx)
      rel, prop ='_', '_'
      if label==0:
        parent_id_str = '_'
      elif label==1:
        rel='same'
      elif label==2:
        parent_id_str, prop = '0', 'OBJ'
      elif label==3:
        rel, prop = 'OBJT', 'OBJ'
      elif label==4:
        rel, prop = 'ATTR', 'ATTR'
      elif label==5:
        rel, prop = 'PRED', 'PRED'
              
      # node_id, node_word, parent_id_str, rel, prop = each
      conll_line = "%d\t%s\t%s\t%s\t%s" % (line_i, words[line_i], parent_id_str, rel, prop,)
      print(conll_line)
      
      if dep_word_idx>len( bpe_word_idx ):
        exit(0)
      
      f_conll.write(conll_line+'\n')
      
    f_conll.write('\n')
    
    #if idx>15: break
    #if idx>9645: break
    #if idx>9820: break
    
    
    
  
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  parser.add_argument('--path',  type=str, default='./bist-parser/preprocess/output/')   
  
  parser.add_argument('--npz',   type=str, default='coco_dev.conll_v32.hdf5_v32.npz')   
  parser.add_argument('--bpe',   type=str, default='coco_dev.conll_v32.bpe')   
  parser.add_argument('--conll', type=str, default='coco_dev.conll_v32')   

  args = parser.parse_args()
  print(args)

  convert_to_conll( args.path+args.npz, args.path+args.bpe, args.path+args.conll)


