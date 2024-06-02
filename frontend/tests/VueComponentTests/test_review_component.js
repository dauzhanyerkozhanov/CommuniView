import { shallowMount } from '@vue/test-utils';
import axios from 'axios';
import Review from '@/components/review.vue';
jest.mock('axios');

describe('Review.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(Review);
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('fetches review on component creation', () => {
    expect(axios.get).toHaveBeenCalledWith('/get', { params: { review_id: wrapper.vm.reviewId } });
  });

  it('submits a new review', () => {
    wrapper.vm.reviewContent = 'This is a test review';
    wrapper.vm.reviewRating = 4;
    wrapper.vm.reviewBusiness = 'Test Business';
    wrapper.vm.submitReview();
    expect(axios.post).toHaveBeenCalledWith('/review', {
      content: wrapper.vm.reviewContent,
      rating_value: wrapper.vm.reviewRating,
      associated_business: wrapper.vm.reviewBusiness
    });
  });

  it('submits a new review with empty content', () => {
    wrapper.vm.reviewContent = '';
    wrapper.vm.reviewRating = 4;
    wrapper.vm.reviewBusiness = 'Test Business';
    wrapper.vm.submitReview();
    expect(axios.post).not.toHaveBeenCalled();
  });

  it('edits an existing review', () => {
    wrapper.vm.reviewId = 1;
    wrapper.vm.reviewContent = 'Updated test review';
    wrapper.vm.reviewRating = 3;
    wrapper.vm.editReview();
    expect(axios.put).toHaveBeenCalledWith('/edit', {
      review_id: wrapper.vm.reviewId,
      content: wrapper.vm.reviewContent,
      rating_value: wrapper.vm.reviewRating
    });
  });

  it('edits an existing review with empty content', () => {
    wrapper.vm.reviewId = 1;
    wrapper.vm.reviewContent = '';
    wrapper.vm.reviewRating = 3;
    wrapper.vm.editReview();
    expect(axios.put).not.toHaveBeenCalled();
  });

  it('deletes a review', () => {
    wrapper.vm.reviewId = 1;
    wrapper.vm.deleteReview();
    expect(axios.delete).toHaveBeenCalledWith('/delete', { data: { review_id: wrapper.vm.reviewId } });
  });

  it('deletes a review with invalid id', () => {
    wrapper.vm.reviewId = null;
    wrapper.vm.deleteReview();
    expect(axios.delete).not.toHaveBeenCalled();
  });
});
