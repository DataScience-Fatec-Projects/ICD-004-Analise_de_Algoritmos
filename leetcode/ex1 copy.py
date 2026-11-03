
class Solution:
    def twoSum(self, nums, target):
        for idx in range(len(nums)):
            sweep_list = 1

            while True:
                next_idx = idx + sweep_list

                if next_idx >= len(nums):
                    break

                if nums[idx] + nums[next_idx] == target:
                    return [idx, next_idx]

                sweep_list += 1

        return []


solution = Solution()

print(solution.twoSum([2, 7, 11, 15], 9))  # [0, 1]
print(solution.twoSum([3, 2, 4], 6))       # [1, 2]
print(solution.twoSum([3, 3], 6))          # [0, 1]
