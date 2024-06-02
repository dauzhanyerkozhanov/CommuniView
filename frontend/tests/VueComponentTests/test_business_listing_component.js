import { shallowMount } from '@vue/test-utils';
import axios from 'axios';
import BusinessListing from '@/vue_components/business_listing.vue';
jest.mock('axios');

describe('BusinessListing.vue', () => {
  let wrapper;
  const mockError = new Error('Network Error');

  beforeEach(() => {
    wrapper = shallowMount(BusinessListing);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('searches for businesses', async () => {
    // Mock the axios get method to return a resolved promise with data
    axios.get.mockResolvedValue({ data: [{ id: '1', name: 'Business 1' }, { id: '2', name: 'Business 2' }] });

    // Set the query data property
    wrapper.setData({ query: 'Business' });

    // Call the search method
    await wrapper.vm.search();

    // Check if axios.get was called with the correct parameters
    expect(axios.get).toHaveBeenCalledWith('/search', { params: { query: 'Business' } });

    // Check if the businesses data property was updated correctly
    expect(wrapper.vm.businesses).toEqual([{ id: '1', name: 'Business 1' }, { id: '2', name: 'Business 2' }]);
  });

  it('handles search error', async () => {
    // Mock the axios get method to return a rejected promise with an error
    axios.get.mockRejectedValue(mockError);

    // Set the query data property
    wrapper.setData({ query: 'Business' });

    // Call the search method
    await wrapper.vm.search();

    // Check if the console.error method was called with the error
    expect(console.error).toHaveBeenCalledWith(mockError);

    // Check if the alert was called with the error message
    expect(window.alert).toHaveBeenCalledWith('An error occurred while searching for businesses.');
  });
});
