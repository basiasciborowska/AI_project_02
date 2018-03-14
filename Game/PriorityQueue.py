
class IndexedPriorityQLow:

	def __init__(self, keys, msize):
		self.vecKeys = keys
		self.heap = [0] * (msize + 1)
		self.invHeap = [0] * (msize + 1)
		self.size = 0
		self.maxSize = msize

	def swap(self, a, b):
	    temp = self.heap[a]
	    self.heap[a] = self.heap[b]
	    self.heap[b] = temp;

	    #change the handles too
	    self.invHeap[self.heap[a]] = a 
	    self.invHeap[self.heap[b]] = b

	def reorderUpwards(self, nd):
	    #move up the heap swapping the elements until the heap is ordered
	    while nd > 1 and self.vecKeys[self.heap[nd / 2]] > self.vecKeys[self.heap[nd]]:
	      	self.swap(nd / 2, nd)
	      	nd /= 2

	def reorderDownwards(self, nd):
		while 2 * nd <= self.size - 1:
			child = 2 * nd
			if child < self.size -1 and self.vecKeys[self.heap[child]] > self.vecKeys[self.heap[child + 1]]:
				child += 1
			if self.vecKeys[self.heap[nd]] > self.vecKeys[self.heap[child]]:
				self.swap(child, nd)
				nd = child
			else:
				break

  	def empty(self):
  		return self.size == 0

  	#to insert an item into the queue it gets added to the end of the heap and then the heap is reordered from the bottom up.
	def insert(self, idx):
		if self.size + 1 <= self.maxSize:
			self.size += 1
			self.heap[self.size] = idx
			self.invHeap[idx] = self.size
			self.reorderUpwards(self.size)
			return True
		return False

	#to get the min item the first element is exchanged with the lowest in the heap and then the heap is reordered from the top down. 
	def pop(self):
	    self.swap(1, self.size)
	    self.reorderDownwards(1)
	    self.size -= 1
	    return self.heap[self.size + 1]

	  #if the value of one of the client key's changes then call this with the key's index to adjust the queue accordingly
	def changePriority(self, idx):
	    self.reorderUpwards(self.invHeap[idx])
