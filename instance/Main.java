import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();

        int[] nums = new int[n];

        // Read input
        for (int i = 0; i < n; i++) {
            nums[i] = sc.nextInt();
        }

        // Bubble Sort
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                if (nums[j] > nums[j + 1]) {
                    int temp = nums[j];
                    nums[j] = nums[j + 1];
                    nums[j + 1] = temp;
                }
            }
        }

        boolean found = false;
                                
        // Find triplets
        for (int i = 0; i < n - 2; i++) {

            // Skip duplicate first elements
            if (i > 0 && nums[i] == nums[i - 1]) {
                continue;
            }

            int left = i + 1;
            int right = n - 1;

            while (left < right) {

                int sum = nums[i] + nums[left] + nums[right];

                if (sum == 0) {

                    System.out.println("[" + nums[i] + ", " + nums[left] + ", " + nums[right] + "]");
                    found = true;

                    // Skip duplicate left values
                    while (left < right && nums[left] == nums[left + 1]) {
                        left++;
                    }

                    // Skip duplicate right values
                    while (left < right && nums[right] == nums[right - 1]) {
                        right--;
                    }

                    left++;
                    right--;

                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }

        if (!found) {
            System.out.println("[]");
        }

        sc.close();
    }
}