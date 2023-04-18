#include <iostream>
#include <vector>

using namespace std;

class MaxHeap {
private:
    vector<int> heap;

    void heapifyUp(int index) {
        int parent = (index - 1) / 2;

        if (index > 0 && heap[index] > heap[parent]) {
            swap(heap[index], heap[parent]);
            heapifyUp(parent);
        }
    }

    void heapifyDown(int index) {
        int left = 2 * index + 1;
        int right = 2 * index + 2;
        int largest = index;

        if (left < heap.size() && heap[left] > heap[largest]) {
            largest = left;
        }

        if (right < heap.size() && heap[right] > heap[largest]) {
            largest = right;
        }

        if (largest != index) {
            swap(heap[index], heap[largest]);
            heapifyDown(largest);
        }
    }

public:
    MaxHeap() {}

    void insert(long val) {
        heap.push_back(val);
        heapifyUp(heap.size() - 1);
    }

    long extractMax() {
        if (heap.empty()) {
            throw out_of_range("Heap is empty");
        }
        int tmp = heap[0];
        heap[0] = heap.back();
        heap.pop_back();
        heapifyDown(0);
        return tmp;
    }

    void deleteMax() {
        if (heap.empty()) {
            throw out_of_range("Heap is empty");
        }
        heap[0] = heap.back();
        heap.pop_back();
        heapifyDown(0);
    }

    bool empty() {
        return heap.empty();
    }

    int size() {
        return heap.size();
    }
};
