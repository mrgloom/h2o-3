package water.exceptions;

import water.H2OError;
import water.util.HttpResponseStatus;

/**
 * This is equivalent to an assertion check that is always performed.
 */
public class H2OMustNotHappenException extends H2OAbstractRuntimeException {
  protected int HTTP_RESPONSE_CODE() { return HttpResponseStatus.INTERNAL_SERVER_ERROR.getCode(); }

  public H2OMustNotHappenException(String message) {
    super(message, message);
  }
}
