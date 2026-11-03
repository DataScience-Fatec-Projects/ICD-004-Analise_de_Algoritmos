class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for idx in range(len(nums)):
            swep_list = 1
            while True:
                next_idx = idx+swep_list
                if next_idx > len(nums) - 1:
                    break #Stop the while
                elif nums[idx] + nums[next_idx] == target:
                     return [idx, next_idx]
                else:                    
                    swep_list+=1
        return [] # There are not a solution to the target
        
solution = Solution 

# Input: nums = [2,7,11,15], target = 9
# Output: [0,1]
nums = [2,7,11,15]
target = 9
result = solution.twoSum(solution , nums, target)
print(result)

# Input: nums = [3,2,4], target = 6
# Output: [1,2]
nums = [3,2,4]
target = 6
result = solution.twoSum(solution , nums, target)
print(result)

# Input: nums = [3,3], target = 6
# Output: [0,1]        
nums = [3,3]
target = 6
result = solution.twoSum(solution , nums, target)
print(result)
