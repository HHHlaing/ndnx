package com.parc.ccn.data.query;

import java.util.ArrayList;

import com.parc.ccn.data.CompleteName;
import com.parc.ccn.data.ContentObject;

public interface CCNInterestListener {
	
	/**
	 * Callback called when we get new results for our query.
	 * @param results Change to a content object, as that is what
	 * 			ccnd is currently handing back anyway.
	 * @return any updates to the standing interest to be expressed
	 */
    public Interest handleContent(ArrayList<ContentObject> results);
    
    /**
     * Notification that our query has timed out.
     * @param query
     */
    public void interestTimedOut(Interest interest);

     /**
     * Returns the queries we are listening for.
     */
    public Interest [] getInterests();
    
    /**
     * This will be called by the repository/query
     * target automatically. Implementations should
     * track interests with a Set or similar method,
     * so that calls to addInterest with the same interest
     * don't result in multiple interests.
     */
    public void addInterest(Interest interest);
    
    /**
     * Does this CompleteName match one of our queries?
     * @param object
     * @return
     */
    public boolean matchesInterest(CompleteName name);
    
    /**
     * Cancel all the queries we are listening to.
     *
     */
    public void cancelInterests();
    
}
