// Import the necessary libraries
import { shallowMount } from '@vue/test-utils';
import axios from 'axios';
import BusinessClaim from '@/components/BusinessClaim.vue';
jest.mock('axios');

describe('BusinessClaim.vue', () => {
  let wrapper;

  beforeEach(() => {
    // Mount the component before each test
    wrapper = shallowMount(BusinessClaim);
  });

  afterEach(() => {
    // Clear all mocks after each test
    jest.clearAllMocks();
  });

  it('submits a claim successfully', async () => {
    // Mock the successful axios post response
    axios.post.mockResolvedValue({ data: { message: 'Claim submitted successfully' } });

    // Set the data properties
    wrapper.setData({
      businessClaim: {
        businessID: '1',
        ownerID: '1',
        claimStatus: 'pending',
        proofDocuments: 'doc.pdf',
        claimId: null
      },
      isSubmitting: false
    });

    // Call the submitClaim method
    await wrapper.vm.submitClaim();

    // Check if axios.post was called with the correct parameters
    expect(axios.post).toHaveBeenCalledWith('/submit_claim', {
      businessID: '1',
      ownerID: '1',
      claimStatus: 'pending',
      proofDocuments: 'doc.pdf'
    });
  });

  it('handles error while submitting a claim', async () => {
    // Mock the axios post error response
    axios.post.mockRejectedValue(new Error('API error'));

    // Call the submitClaim method
    await wrapper.vm.submitClaim();

    // Check if the error message is logged to the console
    expect(console.error).toHaveBeenCalledWith(new Error('API error'));
  });

  it('edits a claim successfully', async () => {
    // Mock the successful axios put response
    axios.put.mockResolvedValue({ data: { message: 'Claim edited successfully' } });

    // Call the editClaim method
    await wrapper.vm.editClaim('1', 'approved');

    // Check if axios.put was called with the correct parameters
    expect(axios.put).toHaveBeenCalledWith('edit_claim/1', { new_status: 'approved' });
  });

  it('handles error while editing a claim', async () => {
    // Mock the axios put error response
    axios.put.mockRejectedValue(new Error('API error'));

    // Call the editClaim method
    await wrapper.vm.editClaim('1', 'approved');

    // Check if the error message is logged to the console
    expect(console.error).toHaveBeenCalledWith(new Error('API error'));
  });

  it('deletes a claim successfully', async () => {
    // Mock the successful axios delete response
    axios.delete.mockResolvedValue({ data: { message: 'Claim deleted successfully' } });

    // Call the deleteClaim method
    await wrapper.vm.deleteClaim('1');

    // Check if axios.delete was called with the correct parameters
    expect(axios.delete).toHaveBeenCalledWith('delete_claim/1');
  });

  it('handles error while deleting a claim', async () => {
    // Mock the axios delete error response
    axios.delete.mockRejectedValue(new Error('API error'));

    // Call the deleteClaim method
    await wrapper.vm.deleteClaim('1');

    // Check if the error message is logged to the console
    expect(console.error).toHaveBeenCalledWith(new Error('API error'));
  });
});
