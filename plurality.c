#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    for(int i = 0; i < candidate_count; i++) {
        if(strcmp(candidates[i].name, name) == 0) {
            candidates[i].votes++;
            return true;
        }
    }

    return false;
}

void merge(candidate arr[], int l, int m, int r)
{
    candidate tgtArr[r - l + 1];
    int idxl = l;
    int idxr = m + 1;
    int idxTgt = 0;

    while(idxl <= m && idxr <= r)
    {
        if(arr[idxl].votes < arr[idxr].votes)
        {
            tgtArr[idxTgt++] = arr[idxl++];
        }
        else
        {
            tgtArr[idxTgt++] = arr[idxr++];
        }
    }


    while(idxl <= m)
    {
        tgtArr[idxTgt++] = arr[idxl++];
    }
    while(idxr <= r)
    {
        tgtArr[idxTgt++] = arr[idxr++];
    }
    for(int i=l;i<=r;++i)
    {
        arr[i] = tgtArr[i-l];
    }
}

void mergeSort(candidate arr[], int l, int r)
{
    if(r > l) {
        int m = (l + r) / 2;
        // left
        mergeSort(arr, l, m);

        // right
        mergeSort(arr, m + 1, r);

        merge(arr, l, m, r);
    }
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    mergeSort(candidates, 0, candidate_count - 1);
    for(int i = candidate_count - 1; i >= 0; i--) {
        if(candidates[i].votes == candidates[candidate_count - 1].votes) {
            printf("%s\n", candidates[i].name);
        } else {
            return;
        }
    }
    return;
}

