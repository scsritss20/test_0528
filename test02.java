test02

package com.suning.common.service;



/**
 * 定义一个类似JS的callback接口
 * @author Administrator
 *
 * @param <T>
 * @param <E>
 */
public interface Function<T, E> {
	T callback(E e);
}